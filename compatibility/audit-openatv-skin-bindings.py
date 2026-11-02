#!/usr/bin/env python3
"""Read-only audit of known native controller fields against named skin screens.

Resolve imported constructor classes and inherited assignments without importing
receiver code. Unknown/dynamic fields are counted, not silently declared safe.
"""
import argparse
import ast
import json
from pathlib import Path
import xml.etree.ElementTree as ET


class NativeIndex:
    def __init__(self, root):
        self.classes = {}
        self.imports = {}
        self.constants = {}
        self.wildcards = {}
        self.parse_errors = []
        self._families = {}
        self._fields = {}
        for path in sorted(root.rglob('*.py')):
            module = '.'.join(path.relative_to(root).with_suffix('').parts)
            if module.endswith('.__init__'):
                module = module[:-9]
            try:
                tree = ast.parse(path.read_text())
            except (OSError, UnicodeError, SyntaxError) as error:
                self.parse_errors.append({'path': str(path.relative_to(root)), 'error': str(error)})
                continue
            names = self.imports.setdefault(module, {})
            self.constants[module] = {}
            self.wildcards[module] = []
            def globals_only(nodes):
                for node in nodes:
                    yield node
                    if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                        for field in ('body', 'orelse', 'finalbody'):
                            yield from globals_only(getattr(node, field, ()))
                        for handler in getattr(node, 'handlers', ()):
                            yield from globals_only(handler.body)
            for node in globals_only(tree.body):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            self.constants[module].setdefault(target.id, set()).add(node.value.value)
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported = node.module
                    if node.level:
                        package = module if path.name == '__init__.py' else module.rpartition('.')[0]
                        parts = package.split('.')
                        imported = '.'.join(parts[:len(parts)-node.level+1] + [node.module])
                    if any(alias.name == '*' for alias in node.names):
                        self.wildcards[module].append(imported)
                    for alias in node.names:
                        names[alias.asname or alias.name] = imported + '.' + alias.name
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        names[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]
                elif isinstance(node, ast.ClassDef):
                    self.classes[module + '.' + node.name] = (module, node)

    def resolve(self, module, expression):
        if isinstance(expression, ast.Name):
            value = self.imports.get(module, {}).get(expression.id, module + '.' + expression.id)
            if value not in self.classes and value.startswith('Plugins.Extensions.') and value[19:] in self.classes:
                value = value[19:]
            if value not in self.classes:
                for imported in self.wildcards.get(module, ()):
                    candidate = imported + '.' + expression.id
                    if candidate in self.classes:
                        return candidate
            return value
        if isinstance(expression, ast.Attribute):
            base = self.resolve(module, expression.value)
            return base + '.' + expression.attr if base else None
        return None

    def templates(self, module, expression, seen=()):
        """Resolve literal, imported and resolution-branch XML without executing code."""
        marker = (module, ast.dump(expression))
        if marker in seen:
            return set()
        seen = seen + (marker,)
        if isinstance(expression, ast.Constant) and isinstance(expression.value, str):
            return {expression.value} if '<screen' in expression.value else set()
        if isinstance(expression, ast.Name):
            result = set(self.constants.get(module, {}).get(expression.id, ()))
            imported = self.imports.get(module, {}).get(expression.id)
            if imported:
                owner, _, name = imported.rpartition('.')
                if owner not in self.constants and owner.startswith('Plugins.Extensions.'):
                    owner = owner[19:]
                result.update(self.templates(owner, ast.Name(id=name), seen))
            for owner in self.wildcards.get(module, ()):
                if owner not in self.constants and owner.startswith('Plugins.Extensions.'):
                    owner = owner[19:]
                result.update(self.templates(owner, expression, seen))
            return {value for value in result if '<screen' in value}
        if isinstance(expression, ast.Attribute):
            owner = self.resolve(module, expression.value)
            if owner in self.classes:
                target_module, cls = self.classes[owner]
                result = set()
                for node in cls.body:
                    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == expression.attr for t in node.targets):
                        result.update(self.templates(target_module, node.value, seen))
                return result
        if isinstance(expression, ast.IfExp):
            return self.templates(module, expression.body, seen) | self.templates(module, expression.orelse, seen)
        if isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.Mod):
            return self.templates(module, expression.left, seen)
        if isinstance(expression, ast.Call) and isinstance(expression.func, ast.Attribute) and expression.func.attr == 'replace':
            try:
                args = [ast.literal_eval(arg) for arg in expression.args]
                if len(args) in (2, 3):
                    return {text.replace(*args) for text in self.templates(module, expression.func.value, seen)}
            except (ValueError, TypeError):
                pass
        return set()

    def family(self, name, visited=()):
        if name in self._families:
            return self._families[name]
        if name in visited:
            return frozenset()
        if name == 'Components.GUIComponent.GUIComponent':
            return frozenset({'gui'})
        if name == 'Components.Element.Element':
            return frozenset({'source'})
        if name not in self.classes:
            return frozenset()
        module, node = self.classes[name]
        result = frozenset().union(*(self.family(self.resolve(module, base), visited + (name,)) for base in node.bases))
        self._families[name] = result
        return result

    def fields(self, name, visited=()):
        if name in self._fields:
            return self._fields[name]
        if name in visited or name not in self.classes:
            return {}
        module, node = self.classes[name]
        fields = {}
        for base in node.bases:
            fields.update(self.fields(self.resolve(module, base), visited + (name,)))
        own = {}
        parents = {child: parent for parent in ast.walk(node) for child in ast.iter_child_nodes(parent)}
        def literals(value):
            try:
                return ast.literal_eval(value)
            except (ValueError, TypeError):
                if isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name) and value.value.id == 'self':
                    for item in ast.walk(node):
                        if isinstance(item, ast.Assign) and any(isinstance(t, ast.Attribute) and t.attr == value.attr for t in item.targets):
                            try:
                                return ast.literal_eval(item.value)
                            except (ValueError, TypeError):
                                pass
                if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == 'range':
                    try:
                        args = [ast.literal_eval(arg) for arg in value.args]
                        result = list(range(*args))
                        return result if len(result) <= 128 else None
                    except (ValueError, TypeError):
                        pass
            return None
        def keys(value, assignment):
            literal = literals(value)
            if isinstance(literal, str):
                return [literal]
            if isinstance(value, ast.Name):
                parent = parents.get(assignment)
                while parent is not None:
                    if isinstance(parent, ast.For) and isinstance(parent.target, ast.Name) and parent.target.id == value.id:
                        return list(literals(parent.iter) or ())
                    parent = parents.get(parent)
            if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Mod) and isinstance(value.left, ast.Constant) and isinstance(value.left.value, str):
                try:
                    return [value.left.value % item for item in keys(value.right, assignment)]
                except (TypeError, ValueError):
                    pass
            return []
        for assignment in ast.walk(node):
            if not isinstance(assignment, ast.Assign) or not isinstance(assignment.value, ast.Call):
                continue
            constructor = self.resolve(module, assignment.value.func)
            if constructor is None:
                continue
            for target in assignment.targets:
                if not (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == 'self'):
                    continue
                for key in keys(target.slice, assignment):
                    if isinstance(key, str):
                        own.setdefault(key, set()).add(constructor)
        fields.update({key: frozenset(value) for key, value in own.items()})
        self._fields[name] = fields
        return fields

    def explicit_aliases(self, name, visited=()):
        if name in visited or name not in self.classes or name == 'Screens.Screen.Screen':
            return None
        module, node = self.classes[name]
        aliases = None
        init = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
        for assignment in ast.walk(init) if init is not None else ():
            if not isinstance(assignment, ast.Assign):
                continue
            if not any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == 'self' and t.attr == 'skinName' for t in assignment.targets):
                continue
            value = assignment.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                aliases = [value.value]
            elif isinstance(value, (ast.List, ast.Tuple)):
                aliases = [x.value if isinstance(x, ast.Constant) and isinstance(x.value, str) else None for x in value.elts]
        if aliases is None:
            for base in node.bases:
                aliases = self.explicit_aliases(self.resolve(module, base), visited + (name,))
                if aliases is not None:
                    break
        return aliases


def active(widget, keys):
    for attr in ('conditional', 'includes'):
        value = widget.get(attr)
        if value and not any(key in keys for key in value.split(',')):
            return False
    return not any(key in keys for key in widget.get('excludes', '').split(',') if key)


def audit(upstream, skin):
    index = NativeIndex(upstream)
    screens = {}
    for screen in ET.parse(skin).getroot().findall('screen'):
        screens.setdefault(screen.get('name'), []).append(screen)
    issues = []
    matched = set()
    unknown = set()
    typed = 0
    for controller in sorted(index.classes):
        fields = index.fields(controller)
        # Native skinName is an ordered fallback list. A class-name template
        # can be deliberately bypassed (Swap), or follow an existing newer
        # template (TimerEditList); do not report those inactive legacy skins.
        aliases = index.explicit_aliases(controller)
        if aliases is None:
            aliases = [index.classes[controller][1].name]
        selected = next((name for name in aliases if name in screens), None)
        for name in [selected] if selected is not None else ():
            matched.add((controller, name))
            for screen in screens[name]:
                for widget in screen.findall('widget'):
                    if not active(widget, fields):
                        continue
                    # A name takes precedence over source in native skin.py.
                    key = widget.get('name') or widget.get('source')
                    if not key or '.' in key:
                        continue
                    constructors = fields.get(key, frozenset())
                    families = [index.family(value) for value in constructors]
                    if len(families) != 1 or not families[0]:
                        unknown.add((controller, name, key))
                        continue
                    typed += 1
                    required = 'gui' if widget.get('name') else 'source'
                    if required not in families[0]:
                        issues.append({'controller': controller, 'screen': name,
                                       'display_id': screen.get('id'), 'field': key,
                                       'binding': 'name' if required == 'gui' else 'source',
                                       'constructor': next(iter(constructors)),
                                       'expected_binding': 'source' if required == 'gui' else 'name'})
    return {'schema': 1, 'matched_controller_screen_pairs': len(matched),
            'typed_widget_bindings_checked': typed,
            'unresolved_or_dynamic_widget_bindings': len(unknown),
            'unresolved_bindings': [{'controller': c, 'screen': s, 'field': k} for c, s, k in sorted(unknown)],
            'parse_errors': index.parse_errors, 'binding_errors': issues,
            'limitations': 'Static imported constructor/inheritance inspection. Dynamic fields, aliases, external plugins and actual GUI rendering require separate validation.'}


def audit_inline(upstream, plugin_roots):
    index = NativeIndex(upstream)
    owners = set()
    for root in plugin_roots:
        plugin = NativeIndex(root)
        owners.update(plugin.classes)
        index.classes.update(plugin.classes)
        index.imports.update(plugin.imports)
        index.constants.update(plugin.constants)
        index.wildcards.update(plugin.wildcards)
        index.parse_errors.extend(plugin.parse_errors)
    issues, unknown, dynamic = [], set(), set()
    checked, templates = 0, 0
    for controller in sorted(owners):
        module, cls = index.classes[controller]
        fields = index.fields(controller)
        for assignment in ast.walk(cls):
            if not isinstance(assignment, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id == 'skin' or isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == 'self' and t.attr == 'skin' for t in assignment.targets):
                continue
            values = index.templates(module, assignment.value)
            if not values:
                dynamic.add(controller)
                continue
            for value in sorted(values):
                try:
                    screen = ET.fromstring(value)
                except ET.ParseError:
                    dynamic.add(controller)
                    continue
                templates += 1
                for widget in screen.findall('widget'):
                    if not active(widget, fields):
                        continue
                    key = widget.get('name') or widget.get('source')
                    if not key or '.' in key:
                        continue
                    constructors = fields.get(key, frozenset())
                    families = [index.family(name) for name in constructors]
                    if len(families) != 1 or not families[0]:
                        unknown.add((controller, key))
                        continue
                    checked += 1
                    required = 'gui' if widget.get('name') else 'source'
                    if required not in families[0]:
                        issues.append({'controller': controller, 'field': key,
                                       'binding': 'name' if required == 'gui' else 'source',
                                       'constructor': next(iter(constructors)),
                                       'expected_binding': 'source' if required == 'gui' else 'name'})
    return {'schema': 1, 'literal_or_imported_templates_checked': templates,
            'typed_widget_bindings_checked': checked,
            'unresolved_or_dynamic_widget_bindings': len(unknown),
            'unresolved_bindings': [{'controller': c, 'field': k} for c, k in sorted(unknown)],
            'dynamic_skin_controllers_requiring_separate_tests': sorted(dynamic),
            'parse_errors': index.parse_errors, 'binding_errors': issues,
            'limitations': 'Literal/imported XML includes conditional resolution imports; generator calls, helper-assigned fields and actual GUI rendering still require separate validation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', required=True, type=Path)
    parser.add_argument('--skin', type=Path, default=Path(__file__).resolve().parents[1] / 'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--plugin-root', action='append', type=Path, help='Audit literal inline plugin skins instead of the shared skin XML')
    args = parser.parse_args()
    result = audit_inline(args.upstream, args.plugin_root) if args.plugin_root else audit(args.upstream, args.skin)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return bool(result['parse_errors'] or result['binding_errors'])


if __name__ == '__main__':
    raise SystemExit(main())
