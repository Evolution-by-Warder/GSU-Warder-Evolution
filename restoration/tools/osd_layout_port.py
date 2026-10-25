"""Use one responsive scrolling skin for the overlay and position preview."""
import ast


def port_osd_layout(source):
    source=source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox','from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil.osd_layout import rolling_skin as _wide_osd_skin, place as _place_osd, right_limit as _osd_right_limit',1)
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef) or cls.name not in ('OnScreenEcmScreen','SelectPosition'):continue
        for method in cls.body:
            if not isinstance(method,ast.FunctionDef):continue
            text=ast.get_source_segment(source,method)
            if method.name=='__init__':
                text=text.replace('self.skin = onScreenEcm_scr','self.skin = _wide_osd_skin(onScreenEcm_scr, getDesktop(0).size().width())')
            elif cls.name=='OnScreenEcmScreen' and method.name=='firstRun':
                text=text.replace('        if self.instance:\n            self.instance.move(ePoint(config.plugins.GlassSysUtil.par1.value, config.plugins.GlassSysUtil.par2.value))','        _place_osd(self, globals())')
            elif cls.name=='SelectPosition' and method.name=='setNewPosition':
                text=text.replace('self.instance.move(ePoint(config.plugins.GlassSysUtil.par1.value, config.plugins.GlassSysUtil.par2.value))','_place_osd(self, globals(), editing=True)')
            elif cls.name=='SelectPosition' and method.name=='right':
                text=text.replace('max(0, getDesktop(0).size().width() - self.instance.size().width())','_osd_right_limit(self, globals())')
            else:continue
            changes.append((method.lineno-1,method.end_lineno,'    '+text+'\n'))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
