"""Replace only CAM download entry with the configured image package feeds."""
import ast


def port_cam_feed(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox', 'from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.cam_feed_ui import initialize as _cam_feed_initialize, load as _cam_feed_load, select as _cam_feed_select',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for node in tree.body:
        if not isinstance(node,ast.ClassDef):continue
        for method in node.body:
            if not isinstance(method,ast.FunctionDef):continue
            if node.name=='univCamMng' and method.name=='moreCamSrv':
                changes.append((method.lineno-1,method.end_lineno,"    def moreCamSrv(self):\n        if self.enCommand == False:\n            self['statCamSrvcmd'].setText(_('Try later ... working'))\n            return\n        self.session.openWithCallback(self.inicializeUCM, ftp_center, None)\n        return\n"))
            if node.name=='ftp_center':
                if method.name=='__init__':
                    statement=next(n for n in method.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr=='wFtp' for t in n.targets))
                    changes.append((statement.end_lineno,statement.end_lineno,"        _cam_feed_initialize(self)\n"))
                elif method.name in ('updatemenulist','doSelection'):
                    function='_cam_feed_load' if method.name=='updatemenulist' else '_cam_feed_select'
                    index=method.body[0].lineno-1
                    changes.append((index,index,"        if self.feedMode:\n            %s(self, globals())\n            return\n"%function))
    for start,end,content in sorted(changes,reverse=True):lines[start:end]=[content]
    return ''.join(lines)
