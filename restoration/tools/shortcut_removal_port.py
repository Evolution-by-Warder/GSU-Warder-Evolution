"""Retire the original global color shortcuts without removing receiver menus."""
import ast


def port_shortcut_removal(source):
    source=source.replace('from Screens.InfoBarGenerics import InfoBarPlugins',
        'from Plugins.Extensions.GlassSysUtil.cam_menu import compact_skin as _compact_cam_menu',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    def replace(node,text):changes.append((node.lineno-1,node.end_lineno,text.rstrip()+'\n'))
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):
            if node.name=='sessionAutostart':
                replace(node,"""def sessionAutostart(reason, **kwargs):
    if reason == 0:
        autocams.autoStartCheck(kwargs['session'])
        OnScreenEcm.startShowOSD(kwargs['session'])
        autoInstallMng.autoInstallStart(kwargs['session'])
    return""")
            elif node.name in ('InfoBarPlugins__init__','keyStartGreen','keyStartRed'):
                replace(node,'def '+node.name+'(self):\n    # Retired: use native Extensions/Event Info menus; never intercept keys.\n    return')
        if not isinstance(node,ast.ClassDef) or node.name!='univCamMng':continue
        for method in node.body:
            if not isinstance(method,ast.FunctionDef):continue
            if method.name=='__init__':
                skin_if=method.body[0]
                changes.append((skin_if.end_lineno,skin_if.end_lineno,'        self.skin = _compact_cam_menu(self.skin)\n'))
                for statement in method.body:
                    if not isinstance(statement,ast.Assign):continue
                    target=ast.unparse(statement.targets[0])
                    if target=="self['txt5']":replace(statement,"        self['txt5'] = Label('')")
                    if target=='self.keyState':replace(statement,'')
                    if target=='self.aa':
                        value=statement.value
                        keep=[i for i,k in enumerate(value.keys) if not isinstance(k,ast.Constant) or k.value!=5]
                        value.keys=[value.keys[i] for i in keep];value.values=[value.values[i] for i in keep]
                        replace(statement,'        self.aa = '+ast.unparse(value))
            elif method.name in ('enaDisKeystart','enaDisKeystartChck'):
                replace(method,'    def '+method.name+'(self):\n        # Retired shortcut setting; retained entry point has no side effects.\n        return')
            elif method.name=='selectFnc':
                text=ast.get_source_segment(source,method)
                text=text.replace('        self.idxAllFnc += 1','        self.idxAllFnc += 1\n        if self.idxAllFnc == 5:\n            self.idxAllFnc += 1',1)
                replace(method,'    '+text)
            elif method.name=='ActivateselectedFnc':
                text=ast.get_source_segment(source,method)
                text=text.replace('        elif self.idxAllFnc == 5:\n            self.enaDisKeystart()\n','',1)
                replace(method,'    '+text)
            elif method.name=='inicializeUCM':
                for statement in method.body:
                    if isinstance(statement,ast.Expr) and ast.unparse(statement)=='self.enaDisKeystartChck()':replace(statement,'')
            elif method.name=='exit':
                check=next(n for n in ast.walk(method) if isinstance(n,ast.If) and ast.unparse(n.test)=='self.keyState != config.plugins.GlassSysUtil.par40.value')
                start=check.orelse[0].lineno-1;end=check.orelse[-1].end_lineno
                replace(check,''.join(line[4:] for line in lines[start:end]))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    source=''.join(lines)
    source=source.replace('ucmInfoBarPlugins__init__ = None\n','',1)
    source=source.replace('config.plugins.GlassSysUtil.par40 = ConfigYesNo(default=False)',
        'config.plugins.GlassSysUtil.par40 = ConfigYesNo(default=False)  # Read old settings only; shortcuts are retired.',1)
    return source
