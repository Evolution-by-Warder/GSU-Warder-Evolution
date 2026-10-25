"""Move the original reader parser behind a background transport, retaining skins."""
import ast


def port_oscam_readers_ui(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox',
        'from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil import oscam_readers_ui as _oscam_readers_ui',1)
    tree=ast.parse(source);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='oscam_readers')
    lines=source.splitlines(keepends=True);changes=[];extra=[]
    for method in cls.body:
        if not isinstance(method,ast.FunctionDef):continue
        body=ast.get_source_segment(source,method)
        if method.name=='__init__':
            body=body.replace("        self['blue_button'] = Label('')","        self['blue_button'] = Label('')\n        _oscam_readers_ui.initialize(self)")
        elif method.name=='oscamreaders':
            marker='        records = _oscam_readers(data)'
            extra.append('    def renderReaders(self, data):\n'+body[body.index(marker):]+'\n')
            body='def oscamreaders(self):\n        _oscam_readers_ui.request(self, globals())'
        elif method.name=='reactivate':
            extra.append('    '+body.replace('def reactivate(self):','def renderReaderDetails(self):',1)+'\n')
            body='def reactivate(self):\n        _oscam_readers_ui.details(self, globals())'
        elif method.name in ('chngState','exit','entitlements'):
            call={'chngState':'change_state(self, globals())','exit':'close(self)','entitlements':'entitlements(self, globals())'}[method.name]
            body='def '+method.name+'(self):\n        _oscam_readers_ui.'+call
        else:continue
        changes.append((method.lineno-1,method.end_lineno,'    '+body+'\n'))
    changes.append((cls.end_lineno,cls.end_lineno,'\n'+'\n'.join(extra)))
    for start,end,body in sorted(changes,reverse=True):lines[start:end]=[body]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
