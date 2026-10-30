#!/usr/bin/env python3
"""Read-only build/CI check; never installed or executed on a receiver.

Check imported exports and reviewed controller signatures/display contracts.
Download only official upstream source files; never import/execute upstream code.
"""
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
from urllib.request import urlopen


def exports(tree):
    result = set()
    def visit(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result.add(node.name)
            return
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            result.update(a.asname or (a.name.split('.')[0] if isinstance(node, ast.Import) else a.name) for a in node.names)
            return
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            result.add(node.id)
        for child in ast.iter_child_nodes(node):
            visit(child)
    visit(tree)
    return result


def display_contract(node):
    result = {}
    for assignment in ast.walk(node):
        if not isinstance(assignment, ast.Assign) or not isinstance(assignment.value, ast.Call):
            continue
        call = assignment.value.func
        if not isinstance(call, ast.Name) or call.id not in ('Label', 'StaticText', 'Input', 'ScrollLabel', 'VirtualKeyboardList', 'Pixmap', 'ProgressBar', 'ConfigList'):
            continue
        for target in assignment.targets:
            if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                try:
                    name = ast.literal_eval(target.slice)
                except (ValueError, TypeError):
                    continue  # Dynamically generated fields are separately reviewed.
                if isinstance(name, str):
                    result[name] = call.id
    return result


def required_widgets(node):
    names = set()
    for call in ast.walk(node):
        if isinstance(call, ast.Call):
            for keyword in call.keywords:
                if keyword.arg == 'mandatoryWidgets':
                    names.update(ast.literal_eval(keyword.value))
    return sorted(names)


def inspect_contract(tree, contract):
    if contract['kind'] == 'epg-config':
        fields = {}
        actions = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                name = ast.unparse(target)
                if name.startswith('config.epgselection.grid') and isinstance(node.value, ast.Call):
                    fields[name] = ast.unparse(node.value.func)
                if name in ('epgActions', 'recActions', 'infoActions') and isinstance(node.value, (ast.List, ast.Tuple)):
                    actions[name] = [entry.elts[0].value for entry in node.value.elts if isinstance(entry, ast.Tuple) and isinstance(entry.elts[0], ast.Constant)]
        return {'fields': fields, 'actions': actions}
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == contract['class'])
    if contract['kind'] == 'display':
        return {'components': display_contract(node), 'mandatory_widgets': required_widgets(node)}
    method = next(n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == contract['method'])
    # ast.dump started omitting empty fields by default in Python 3.13.
    # The source signature stays comparable across our 3.9/3.14 CI runtimes.
    return ast.unparse(method.args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--upstream', type=Path, help='OpenATV lib/python directory')
    parser.add_argument('--ref', default='master')
    parser.add_argument('--cache-dir', type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    paths = sorted(set(manifest['modules']) | {c['module'] for c in manifest['contracts']})
    def read(module):
        path = module.replace('.', '/') + '.py'
        if args.upstream:
            return module, (args.upstream / path).read_bytes()
        url = 'https://raw.githubusercontent.com/openatv/enigma2/%s/lib/python/%s' % (args.ref, path)
        with urlopen(url, timeout=45) as response:
            data = response.read(4 * 1024 * 1024)
        if args.cache_dir:
            target = args.cache_dir / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return module, data
    try:
        with ThreadPoolExecutor(max_workers=6) as pool:
            trees = {module: ast.parse(data) for module, data in pool.map(read, paths)}
        failures = []
        for module, names in manifest['modules'].items():
            missing = set(names) - exports(trees[module])
            if missing:
                failures.append('%s: missing imported exports %s' % (module, sorted(missing)))
        for contract in manifest['contracts']:
            label = '%s.%s%s' % (contract['module'], contract.get('class', contract['kind']), '.' + contract['method'] if 'method' in contract else '')
            try:
                if inspect_contract(trees[contract['module']], contract) != contract['expected']:
                    failures.append(label + ': reviewed interface changed; review compatibility before release')
            except (StopIteration, TypeError, ValueError):
                failures.append(label + ': reviewed controller/method contract is missing')
        if failures:
            print('\n'.join(failures), file=sys.stderr)
            return 1
        print('PASS: %s, %d imported exports in %d modules, %d controller contracts (%s)' % (
            manifest['project'], sum(map(len, manifest['modules'].values())), len(manifest['modules']), len(manifest['contracts']), args.upstream or args.ref))
        return 0
    except (OSError, SyntaxError, ValueError) as error:
        print('OpenATV interface check could not complete: %s' % error, file=sys.stderr)
        return 1  # Network or syntax failure cannot silently approve a release.


if __name__ == '__main__':
    raise SystemExit(main())
