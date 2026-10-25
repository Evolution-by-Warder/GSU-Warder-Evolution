"""Reproducible, scoped native SoftCAM hooks for the original CAM manager."""
import ast


def port_native_softcam(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox', 'from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.native_softcam import NativeSoftcam, handle_action as _native_softcam_action',1)
    tree=ast.parse(source)
    screen=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='univCamMng')
    lines=source.splitlines(keepends=True)
    inserts=[]
    hooks={
        'getCamName': "        if self.nativeSoftcam.running():\n            return self.nativeSoftcam.selected()\n",
        'checkStatCam': "        if self.nativeSoftcam.selected():\n            self.CamSrvMsg(_('CAM/SRV Running') if self.nativeSoftcam.running() else _('No Running CAM/SRV'))\n            return True\n",
        'start': "        if _native_softcam_action(self, 'start', eConsoleAppContainer, _):\n            return\n",
        'stop': "        if _native_softcam_action(self, 'stop', eConsoleAppContainer, _):\n            return\n",
    }
    for node in screen.body:
        if not isinstance(node,ast.FunctionDef):continue
        if node.name in hooks:inserts.append((node.body[0].lineno-1,hooks[node.name]))
        if node.name=='__init__':
            statement=next(n for n in node.body if isinstance(n,ast.Expr) and 'Screen.__init__' in ast.unparse(n))
            inserts.append((statement.end_lineno,"        self.nativeSoftcam = NativeSoftcam()\n"))
        if node.name=='CamSrvList':
            statement=next(n for n in node.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='selCam' for t in n.targets))
            inserts.append((statement.lineno-1,"        native = self.nativeSoftcam.selected()\n        if native:\n            Cam.append(native)\n            self.Cam_list[native] = '@native-softcam'\n"))
    for index,content in sorted(inserts,reverse=True):lines.insert(index,content)
    return ''.join(lines)
