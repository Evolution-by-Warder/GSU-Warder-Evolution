"""Remove obsolete image preparation completely, as requested by the maintainer."""
import ast


def remove_exp_image(source):
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    screen=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='univCamMng')
    for method in screen.body:
        if not isinstance(method,ast.FunctionDef):continue
        if method.name in ('killDccamd','doLnk','chckDccamd'):
            changes.append((method.lineno-1,method.end_lineno,''));continue
        if method.name=='__init__':
            for node in method.body:
                if not isinstance(node,ast.Assign):continue
                target=ast.unparse(node.targets[0])
                if target in ("self['txt9']",'self.enaYellow'):changes.append((node.lineno-1,node.end_lineno,''))
                if target=='self.aa':
                    pairs=[(k,v) for k,v in zip(node.value.keys,node.value.values) if not isinstance(k,ast.Constant) or k.value!=9]
                    value=ast.Dict(keys=[k for k,v in pairs],values=[v for k,v in pairs])
                    changes.append((node.lineno-1,node.end_lineno,'        self.aa = '+ast.unparse(value)+'\n'))
        if method.name=='ActivateselectedFnc':
            node=next(n for n in ast.walk(method) if isinstance(n,ast.If) and ast.unparse(n.test)=='self.idxAllFnc == 9')
            changes.append((node.lineno-1,node.end_lineno,''))
        if method.name=='selectFnc':
            node=next(n for n in method.body if isinstance(n,ast.If) and ast.unparse(n.test)=='self.idxAllFnc > 9')
            changes.append((node.lineno-1,node.lineno,lines[node.lineno-1].replace('> 9','> 8')))
        if method.name=='inicializeUCM':
            for node in method.body:
                if isinstance(node,ast.Expr) and ast.unparse(node)=="self['txt9'].color2()":changes.append((node.lineno-1,node.end_lineno,''))
                if isinstance(node,ast.If) and ast.unparse(node.test) in ("self.chckDccamd()","not os.path.exists('/usr/keys')","not os.path.exists('/var/etc')"):
                    changes.append((node.lineno-1,node.end_lineno,''))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
