"""Add the selected Warder diagnostics to the original main menu."""
import ast


def port_warder_tools(source):
    source='from Plugins.Extensions.GlassSysUtil import warder_tools_ui as _warder_tools_ui\n'+source
    tree=ast.parse(source);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='SysUtilMngMain')
    lines=source.splitlines(keepends=True);changes=[]
    for node in ast.walk(cls):
        if isinstance(node,ast.Assign) and any(ast.unparse(t)=='self.menuListAll' for t in node.targets):
            last=node.value.elts[-1]
            changes.append((last.lineno-1,last.lineno-1,"            ('17', _warder_tools_ui.text(globals(), 'Tools'), _warder_tools_ui.text(globals(), 'System overview and a diagnostic file for support.')),\n"))
        if isinstance(node,ast.If) and ast.unparse(node.test)=="selectedItem == '16'":
            changes.append((node.lineno-1,node.lineno-1,"            elif selectedItem == '17':\n                _warder_tools_ui.open_tools(self.session, globals())\n"))
    for start,end,value in sorted(changes,reverse=True):lines[start:end]=[value]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
