"""Connect native running/stopped status to the existing CAM status icon."""
import ast


def port_cam_status(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox','from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.native_status import request as _native_status_request',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    screen=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='univCamMng')
    for method in screen.body:
        if not isinstance(method,ast.FunctionDef):continue
        if method.name=='chckOscam':
            changes.append((method.body[0].end_lineno,method.body[0].end_lineno,'        _native_status_request(self, _)\n'))
        if method.name=='checkStatCam':
            statement=method.body[0].body[0]
            changes.append((statement.lineno-1,statement.lineno-1,"            active = self.nativeSoftcam.active_name()\n            self.statcommPics('stat', 'green' if active else 'red')\n"))
            line=lines[statement.lineno-1].replace('self.nativeSoftcam.active_name()','active')
            changes.append((statement.lineno-1,statement.end_lineno,line))
            for node in method.body:
                if isinstance(node,ast.Expr) and ast.unparse(node)=="self.statcommPics('stat', 'blue')":
                    changes.append((node.lineno-1,node.end_lineno,"        self.statcommPics('stat', 'red')\n"))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    return ''.join(lines)
