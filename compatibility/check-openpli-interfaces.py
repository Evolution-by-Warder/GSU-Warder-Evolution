#!/usr/bin/env python3
"""Check actual Enigma2 imports/call shapes against a supplied official source tree.

No upstream code is imported. This does not validate C++ ABI, dynamic attribute
calls, hardware, networking or physical rendering. Guarded imports are reported.
"""
import argparse
import ast
from functools import lru_cache
import inspect
import json
from pathlib import Path

PREFIXES=('Components','Screens','Tools','ServiceReference','skin')

@lru_cache(None)
def parse(path):
    return ast.parse(path.read_bytes())

def exports(tree):
    names=set()
    def visit(node):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            names.add(node.name);return
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            names.update(a.asname or (a.name.split('.')[0] if isinstance(node,ast.Import) else a.name) for a in node.names)
            return
        if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Store):names.add(node.id)
        for child in ast.iter_child_nodes(node):visit(child)
    visit(tree)
    return names

def resolve(roots,module):
    for root in roots:
        for suffix in ('.py','/__init__.py'):
            path=root/(module.replace('.','/')+suffix)
            if path.is_file():return path

def signature(node):
    args=node.args;pos=args.posonlyargs+args.args
    defaults=[inspect.Parameter.empty]*(len(pos)-len(args.defaults))+[None]*len(args.defaults)
    params=[inspect.Parameter(arg.arg,inspect.Parameter.POSITIONAL_ONLY if arg in args.posonlyargs else inspect.Parameter.POSITIONAL_OR_KEYWORD,default=default) for arg,default in zip(pos,defaults)]
    if args.vararg:params.append(inspect.Parameter(args.vararg.arg,inspect.Parameter.VAR_POSITIONAL))
    params.extend(inspect.Parameter(arg.arg,inspect.Parameter.KEYWORD_ONLY,default=inspect.Parameter.empty if default is None else None) for arg,default in zip(args.kwonlyargs,args.kw_defaults))
    if args.kwarg:params.append(inspect.Parameter(args.kwarg.arg,inspect.Parameter.VAR_KEYWORD))
    return inspect.Signature(params)

def guarded(node,parents):
    while node in parents:
        parent=parents[node]
        if isinstance(parent,ast.Try) and node in parent.body:
            for handler in parent.handlers:
                if handler.type is None:return True
                types=handler.type.elts if isinstance(handler.type,ast.Tuple) else [handler.type]
                if any(isinstance(t,ast.Name) and t.id in ('ImportError','ModuleNotFoundError','Exception','BaseException') for t in types):return True
        node=parent
    return False

def scan(root,upstream):
    report={'source_files':0,'import_statements':0,'calls_checked':0,'dynamic_calls':0,
            'missing_imports':[],'guarded_imports':[],'inactive_legacy_imports':[],'invalid_calls':[]}
    for path in sorted(root.rglob('*.py')):
        report['source_files']+=1;tree=parse(path);parents={child:parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)};imports={}
        for node in ast.walk(tree):
            if not isinstance(node,ast.ImportFrom) or node.level or not node.module or not node.module.startswith(PREFIXES):continue
            report['import_statements']+=1;target=resolve((root,upstream),node.module)
            absent=[]
            if target:
                names=exports(parse(target))
                absent=[a.name for a in node.names if a.name!='*' and a.name not in names and not (target.parent/(a.name+'.py')).exists()]
                definitions={n.name:n for n in parse(target).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
                for alias in node.names:
                    if alias.name=='*':imports.update(definitions)
                    elif alias.name in definitions:imports[alias.asname or alias.name]=definitions[alias.name]
            if target is None or absent:
                entry={'file':path.relative_to(root).as_posix(),'line':node.lineno,'module':node.module,'missing':absent if target else ['<module>']}
                category='guarded_imports' if guarded(node,parents) else 'missing_imports'
                # This shipped historical replacement is deliberately inactive:
                # never swap OpenPLi's own Menu.py for Menu-new17.py.
                if entry['file']=='Screens/Menu-new17.py' and node.module=='Screens.Setup' and absent==['getSetupTitle']:
                    plugin=root/'Plugins/Extensions/setupGlass17/plugin.py'
                    if plugin.is_file():
                        fn=next((n for n in parse(plugin).body if isinstance(n,ast.FunctionDef) and n.name=='setMenuPyo'),None)
                        guard=next((n for n in fn.body if isinstance(n,ast.If)),None) if fn else None
                        if guard and '_WarderOpenPli' in ast.unparse(guard.test) and isinstance(guard.body[0],ast.Return) and isinstance(guard.body[0].value,ast.Constant) and guard.body[0].value.value is False:category='inactive_legacy_imports'
                report[category].append(entry)
        for node in ast.walk(tree):
            if not isinstance(node,ast.Call):continue
            target=None;extra=[]
            if isinstance(node.func,ast.Name):
                target=imports.get(node.func.id)
                if isinstance(target,ast.ClassDef):
                    target=next((n for n in target.body if isinstance(n,ast.FunctionDef) and n.name=='__init__'),None)
                    if target:extra=[None]
            elif isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name):
                cls=imports.get(node.func.value.id)
                if isinstance(cls,ast.ClassDef):target=next((n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name==node.func.attr),None)
            if not isinstance(target,ast.FunctionDef):continue
            if any(isinstance(a,ast.Starred) for a in node.args) or any(k.arg is None for k in node.keywords):report['dynamic_calls']+=1;continue
            report['calls_checked']+=1
            try:signature(target).bind(*extra,*[None]*len(node.args),**{k.arg:None for k in node.keywords})
            except TypeError as error:report['invalid_calls'].append({'file':path.relative_to(root).as_posix(),'line':node.lineno,'call':ast.unparse(node.func),'error':str(error),'signature':str(signature(target))})
    report['limitations']='Static Python imports and directly imported callable shapes; dynamic dispatch, wildcard names and C++ exports/ABI require separate validation. No receiver execution.'
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin-root',required=True,type=Path)
    parser.add_argument('--upstream',required=True,type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();report=scan(args.plugin_root,args.upstream)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
    failures=report['missing_imports']+report['invalid_calls']
    if failures:print(json.dumps(failures,indent=2))
    print('%s: %d files, %d imports, %d direct calls; %d guarded imports, %d inactive legacy imports, %d failures' % ('FAIL' if failures else 'PASS',report['source_files'],report['import_statements'],report['calls_checked'],len(report['guarded_imports']),len(report['inactive_legacy_imports']),len(failures)))
    return bool(failures)

if __name__=='__main__':raise SystemExit(main())
