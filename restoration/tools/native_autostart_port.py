"""Reproduce native session-start handling without changing legacy entry names."""
import ast


def port_native_autostart(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox','from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.native_autostart import begin as _native_autostart_begin',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for node in tree.body:
        if isinstance(node,ast.ClassDef) and node.name=='AutoCams':
            method=next(m for m in node.body if isinstance(m,ast.FunctionDef) and m.name=='autoStartCheck')
            changes.append((method.body[0].end_lineno,"        if _native_autostart_begin(self, globals()):\n            return\n"))
        if isinstance(node,ast.FunctionDef) and node.name=='sessionAutostart':
            changes.append((node.body[0].lineno-1,"    if reason != 0:\n        delayed = getattr(autocams, 'nativeDelayedStart', None)\n        if delayed:\n            delayed.cancel()\n"))
    for index,content in sorted(changes,reverse=True):lines.insert(index,content)
    return ''.join(lines)
