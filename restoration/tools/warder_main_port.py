"""Apply the first Warder presentation step to the restored r40 main screen."""
import ast


def port_warder_main(source):
    if 'import warder_main as _warder_main' in source:return source
    source=source.replace("icon='SysMgt.png'", "icon='images/warder-plugin.png'")
    source='from Plugins.Extensions.GlassSysUtil import warder_main as _warder_main\n'+source
    tree=ast.parse(source)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='SysUtilMngMain')
    lines=source.splitlines(keepends=True);changes=[]
    for method in cls.body:
        if not isinstance(method,ast.FunctionDef):continue
        for node in ast.walk(method):
            if method.name=='__init__' and isinstance(node,ast.Assign):
                target=ast.unparse(node.targets[0])
                if target=='self.skin':
                    changes.append((node.lineno-1,node.end_lineno,"        desktop = getDesktop(0).size()\n        self.skin = _warder_main.main_skin(desktop.width(), desktop.height()) if desktop.width() >= 1280 else SysUtilMngMain.skin\n"))
                if target=='self.size':
                    changes.append((node.end_lineno,node.end_lineno,"        _warder_main.install(self, globals())\n"))
            if method.name=='updatemenulist' and isinstance(node,ast.Assign) and ast.unparse(node.targets[0])=='item':
                # Replace the old text/pixmap construction but keep IDs, enable tests and list semantics.
                loop=next(n for n in ast.walk(method) if isinstance(n,ast.For))
                append=next(n for n in loop.body if isinstance(n,ast.Expr) and ast.unparse(n).startswith('self.list.append(item)'))
                changes.append((node.lineno-1,append.end_lineno,"            desktop = getDesktop(0).size()\n            self.list.append(_warder_main.menu_row(globals(), x[0], x[1], self.status[x[0]], desktop.width(), desktop.height()))\n"))
            if method.name=='reactivate' and isinstance(node,ast.Expr) and ast.unparse(node).startswith("self['info'].setText"):
                changes.append((node.end_lineno,node.end_lineno,"            _warder_main.selection(self, entry)\n"))
            if method.name=='updatemenulist' and isinstance(node,ast.Expr) and ast.unparse(node)=="self['list'].l.setList(self.list)":
                changes.append((node.end_lineno,node.end_lineno,"        self.reactivate()\n"))
    for start,end,value in sorted(changes,reverse=True):lines[start:end]=[value]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
