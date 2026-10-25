"""Reproducible conditional standalone-server UI, retaining original entry points."""
import ast


def port_srv_visibility(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox','from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.srv_visibility import apply as _srv_visibility, prepare_skin as _srv_skin, binary_status as _srv_binary_status, menu_text as _cam_menu_text',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    screen=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='univCamMng')
    for method in screen.body:
        if not isinstance(method,ast.FunctionDef):continue
        if method.name=='__init__':
            skin=next(n for n in method.body if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=='self.skin' and isinstance(n.value,ast.Call))
            changes.append((skin.end_lineno,skin.end_lineno,'        self.skin = _srv_skin(self.skin)\n'))
            native=next(n for n in method.body if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=='self.nativeSoftcam')
            changes.append((native.end_lineno,native.end_lineno,"        self.numSrv = 0\n        self['srvArrowLeft'] = Pixmap()\n        self['srvArrowRight'] = Pixmap()\n"))
        if method.name=='selectFnc':
            statement=next(n for n in method.body if isinstance(n,ast.If) and ast.unparse(n.test)=='self.idxAllFnc == 5')
            changes.append((statement.end_lineno,statement.end_lineno,'        if self.idxAllFnc == 7 and not self.numSrv:\n            self.idxAllFnc += 1\n'))
        if method.name=='ActivateselectedFnc':
            changes.append((method.body[0].lineno-1,method.body[0].lineno-1,'        if self.idxAllFnc == 7 and not self.numSrv:\n            return\n'))
        if method.name=='CamSrvList':
            for node in ast.walk(method):
                if isinstance(node,ast.Expr) and ast.unparse(node).startswith("self.list.append(getConfigListEntry(_('SRVs')"):
                    text=ast.get_source_segment(source,node)
                    changes.append((node.lineno-1,node.end_lineno,'        if self.numSrv:\n            '+text+'\n'))
                if isinstance(node,ast.If) and ast.unparse(node.test)=="'_Srv.sh' in x":
                    line=lines[node.lineno-1].replace("'_Srv.sh' in x","x.endswith('_Srv.sh')")
                    changes.append((node.lineno-1,node.lineno,line))
            changes.append((method.body[-1].lineno-1,method.body[-1].lineno-1,'        _srv_visibility(self, globals())\n'))
        if method.name=='checkSrvBin':
            changes.append((method.lineno-1,method.end_lineno,"    def checkSrvBin(self, srv):\n        status = _srv_binary_status(srv)\n        return 'Ok' if status == 'Ok' else srv + '_Srv.sh ' + _(status)\n"))
        if method.name=='statcommPics':
            changes.append((method.body[0].lineno-1,method.body[0].lineno-1,"        if statcom == 'picsrv' and not getattr(self, 'numSrv', 0):\n            self['SrvPic'].hide()\n            return\n"))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    source=''.join(lines)
    # Preserve original gettext keys; alter only combined CAM/SRV captions.
    tree=ast.parse(source);screen=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='univCamMng')
    offsets=[0]
    for line in source.splitlines(keepends=True):offsets.append(offsets[-1]+len(line.encode()))
    raw=source.encode();calls=[]
    for node in ast.walk(screen):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='_' and len(node.args)==1 and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str) and 'CAM/SRV' in node.args[0].value:
            start=offsets[node.lineno-1]+node.col_offset;end=offsets[node.end_lineno-1]+node.end_col_offset
            calls.append((start,end,('_cam_menu_text(self, _, '+ast.unparse(node.args[0])+')').encode()))
    for start,end,text in sorted(calls,reverse=True):raw=raw[:start]+text+raw[end:]
    return raw.decode()
