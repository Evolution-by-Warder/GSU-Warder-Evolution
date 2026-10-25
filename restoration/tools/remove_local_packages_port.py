"""Retire the general installer/scripts section; retain CAM package removal."""
import ast

RETIRED={'ipk_script_center','script_center','ipk_center','tar_center'}


def remove_local_packages(source):
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef):continue
        if cls.name in RETIRED:
            changes.append((cls.lineno-1,cls.end_lineno,''));continue
        if cls.name=='SysUtilMngMain':
            for node in ast.walk(cls):
                if isinstance(node,ast.Assign) and any(ast.unparse(t)=='self.menuListAll' for t in node.targets):
                    for item in node.value.elts:
                        if item.elts[0].value=='5':changes.append((item.lineno-1,item.end_lineno,''))
                if isinstance(node,ast.If) and ast.unparse(node.test)=="selectedItem == '5'":
                    changes.append((node.lineno-1,node.body[-1].end_lineno,''))
        if cls.name=='ipk_uninstall_center':
            # This original class is also the CAM manager's package removal UI.
            for method in cls.body:
                if not isinstance(method,ast.FunctionDef):continue
                body=ast.get_source_segment(source,method)
                if method.name=='__init__':
                    body=body.replace('self.what = what',"self.what = what or 'ucm'")
                elif method.name=='updateList':
                    body='''def updateList(self):
        self.setWindowTitle(_('Uninstall CAM/SRV menu'))
        self.list = []
        for line in chckPckgList():
            if line.startswith('glasssysutil-') or _is_cam_package(line.split(' - ', 1)[0]):
                item = [line]
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(860), fhd(25)), font=0, text=line))
                led = 'blue' if '-srv.' in line else 'yellow'
                item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=LoadPixmap(BP_ICO % led)))
                self.list.append(item)
        if not self.list:
            self.list = [['None', MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=_('No CAM/SRV installed'))]]
        self['list'].l.setList(self.list)
'''
                else:continue
                changes.append((method.lineno-1,method.end_lineno,'    '+body+'\n'))
    for start,end,body in sorted(changes,reverse=True):lines[start:end]=[body]
    result=''.join(lines);compile(result,'plugin.py','exec');return result
