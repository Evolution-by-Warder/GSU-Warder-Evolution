"""Repair recovered OSD control flow while retaining its original display modes."""
import ast


def restore_osd(source):
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef):continue
        for method in cls.body:
            if not isinstance(method,ast.FunctionDef):continue
            text=ast.get_source_segment(source,method)
            if cls.name=='OnScreenEcmScreen':
                if method.name=='__init__':
                    text=text.replace("            else:\n                self.e =", "            self.e =",1)
                    # These three assignments were wrongly inside try/else.
                    body=text.splitlines()
                    for i,line in enumerate(body):
                        if line.startswith("                self['ecm_items']") or line.startswith("                self['OSD_Ecm_info']"):
                            body[i]=line[4:]
                    text='\n'.join(body).replace("        self.onShow.append(self.firstRun)","        self.onShow.append(self.firstRun)\n        self.onLayoutFinish.append(self.prepareOsd)")
                    text=text.replace('        self.allInfos = {}','        self.cryptService = False\n        self.allInfos = {}',1)
                elif method.name=='readEcmInfo':
                    body=text.splitlines();start=next(i for i,line in enumerate(body) if line.strip()=='self.ecmInfo_time = ecmInfo_time')
                    end=next(i for i,line in enumerate(body[start:],start) if line.strip()=='isneedShow = False')
                    for i in range(start,end):
                        if body[i].startswith('    '):body[i]=body[i][4:]
                    # The static/rolling error choice was also recovered incorrectly.
                    using=next(i for i,line in enumerate(body) if "if using == 'unsupported CAs" in line)
                    body[using+1:using+5]=[
                        '                if config.plugins.GlassSysUtil.par3.value:',
                        "                    self.staticEcmStart('\\n***    ' + _('Unsuported CA found, incorrect ECM info') + '    ***')",
                        '                else:',
                        "                    self.StartrollTextInfo('   ***    ' + _('Unsuported CA found, incorrect ECM info') + '    ***')",
                        '                return']
                    text='\n'.join(body)
                    text=text.replace('if not config.plugins.GlassSysUtil.par0.value:', 'if not config.plugins.GlassSysUtil.par0.value or not self.cryptService:',1)
                    text=text.replace("                        ecmOldtmp = abs(float(ecmOldtmp[:-1]) - float(ecmTime[:-1]))\n                        if len(ecmTime[:-1]) > 3:\n                            ecmOldtmp *= 1000", "                        ecmOldtmp = abs(float(ecmOldtmp[:-1]) - float(ecmTime[:-1])) * 1000")
                    text=text.replace("            if config.plugins.GlassSysUtil.par3.value or tmpline != '':", "            if not config.plugins.GlassSysUtil.par3.value and isneedShow and tmpline != '':")
                    text=text.replace("self.StartrollTextInfo('                                           ' + tmpline + '   ')", "self.StartrollTextInfo('   ' + tmpline + '   ')")
                    text=text.replace('            elif isneedShow:', '            elif config.plugins.GlassSysUtil.par3.value and isneedShow:')
                elif method.name=='__endShow':
                    body=text.splitlines();end=next(i for i,line in enumerate(body) if line.startswith('        if not config.plugins.GlassSysUtil.par3'))
                    body[1:end]=[line[4:] for line in body[2:end]]
                    body.insert(1,'        self.ecmInfo_time = None')
                    body.insert(1,'        self.cryptService = False')
                    text='\n'.join(body)
                elif method.name=='__startSearchInfo':
                    text=text.replace('        if config.plugins.GlassSysUtil.par0.value:', '        self.cryptService = False\n        if config.plugins.GlassSysUtil.par0.value:',1)
                    text=text.replace("                    self.sid =", "                    self.cryptService = True\n                    self.sid =",1)
                    text=text.replace('                    self.staticEcmStart()',"                    self['ecm_items'].setText('')\n                    self['OSD_Ecm_info'].setText(_('Free To Air'))\n                    self.staticEcmStart()\n            else:\n                OnScreenEcm.makeShow('hide')",1)
                    text=text.replace("'                                      ***", "'   ***")
                else:continue
            elif cls.name=='OnScreenEcmMain' and method.name=='makeShow':
                text=text.replace("        if whatDo == 'None':", "        if self.dialog is None:\n            return\n        if whatDo == 'None':",1)
                text=text.replace('                self.dialog.hide()', '                self.dialog._OnScreenEcmScreen__endShow()',1)
            elif cls.name=='SelectPosition':
                if method.name in ('ok','exit'):
                    text=text.replace('        self.moveTimer = None','        self.moveTimer.stop()\n        self.moveTimer = None',1)
                elif method.name=='right':text=text.replace('fhd(1180)','max(0, getDesktop(0).size().width() - self.instance.size().width())')
                elif method.name=='down':text=text.replace('fhd(700)','max(0, getDesktop(0).size().height() - self.instance.size().height())')
                else:continue
            elif cls.name=='OSD_ECM_Menu' and method.name in ('saveOnly','exitCancel'):
                action='save' if method.name=='saveOnly' else 'cancel'
                text=text.replace("        for x in self['config'].list:\n            x[1]."+action+"()", "        for key in ('par0', 'par4', 'par5', 'par78', 'par80', 'par81'):\n            getattr(config.plugins.GlassSysUtil, key)."+action+"()",1)
            else:continue
            changes.append((method.lineno-1,method.end_lineno,'    '+text+'\n'))
        if cls.name=='OnScreenEcmScreen':
            changes.append((cls.end_lineno,cls.end_lineno,"\n    def prepareOsd(self):\n        for name in ('OSD_Ecm_info', 'ecm_items'):\n            if name in self:\n                self[name].instance.setWrap(0)\n"))
    for start,end,text in sorted(changes,reverse=True):lines[start:end]=[text]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
