"""Scoped hooks for native CAM package updates and removals."""
import ast


def port_cam_management(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox','from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.cam_package_actions import controls as _cam_package_controls, update as _cam_package_update, remove as _cam_package_remove, is_cam_package as _is_cam_package',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for screen in tree.body:
        if not isinstance(screen,ast.ClassDef):continue
        for method in screen.body:
            if not isinstance(method,ast.FunctionDef):continue
            if screen.name=='univCamMng':
                if method.name=='chckOscam':
                    index=method.body[0].end_lineno
                    changes.append((index,index,"        if _cam_package_controls(self):\n            self.chckOscamTimer.start(500)\n            return\n"))
                if method.name=='setLatestOscam':
                    index=method.body[0].lineno-1
                    changes.append((index,index,"        if _cam_package_update(self, globals()):\n            return\n"))
            if screen.name=='ipk_uninstall_center':
                if method.name=='uninstallIpk':
                    index=method.body[0].lineno-1
                    changes.append((index,index,"        if answer and _cam_package_remove(self, globals()):\n            return\n"))
                if method.name=='updateList':
                    for n in ast.walk(method):
                        if isinstance(n,ast.If) and ast.unparse(n.test)=="line.startswith('glasssysutil-')":
                            index=n.lineno-1
                            changes.append((index,index+1,lines[index].replace("line.startswith('glasssysutil-')","line.startswith('glasssysutil-') or _is_cam_package(line.split(' - ', 1)[0])")))
    for start,end,content in sorted(changes,reverse=True):lines[start:end]=[content]
    return ''.join(lines)
