"""One Warder-styled local backup workspace; no network or implicit restore."""
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap
from xml.etree import ElementTree as ET

from .warder_screen import Screen
from . import warder_dashboard as dashboard, warder_backup as backup
from .i18n import for_api


class BackupMenu(Screen):
    def __init__(self,session,api):
        self.api=api
        self.width,self.height=dashboard.dimensions(api)
        root=ET.fromstring(dashboard.skin(self.width,self.height,'menu'))
        root.set('name','WarderBackupMenu')
        for node in list(root):
            if node.get('name','').startswith('inline_'):root.remove(node)
        self.skin=ET.tostring(root,encoding='unicode')
        Screen.__init__(self,session)
        dashboard.install_header(self,api)
        self.selected=set(backup.PRODUCTS)
        self.locations=[]
        self.location=0
        self.browsing=False
        self.paths=[]
        self.preview=None
        self.snapshot={}
        self['list']=api['ListboxSys2']([])
        self['list'].l.setFont(0,api['gFont']('Regular',round(28*self.height/1080)))
        self['list'].l.setItemHeight(round(74*self.height/1080))
        self['list'].onSelectionChanged.append(self.describe)
        for name in ('heading','result_title','result_status','red','green','yellow','blue'):
            self[name]=Label('')
        self['descriptions']=ScrollLabel('')
        self['actions']=ActionMap(['ColorActions','SetupActions','DirectionActions'],
            {'red':self.back,'cancel':self.back,'back':self.back,'ok':self.select,
             'green':self.execute,'yellow':self.destination,'blue':self.browse,
             'up':self['list'].up,'down':self['list'].down,
             'left':self['descriptions'].pageUp,'right':self['descriptions'].pageDown},-2)
        self.onLayoutFinish.append(self.refresh)

    def tr(self,key):return for_api(self.api,key)

    def directory(self):
        return self.locations[self.location] if self.locations else None

    def refresh(self):
        current=self.directory()
        self.locations=backup.destinations()
        self.location=self.locations.index(current) if current in self.locations else 0
        self.snapshot=backup.snapshot(self.api['config'])
        self.render()

    def render(self,index=0):
        tr=self.tr
        self['heading'].setText(tr('Backup and restore'))
        self['red'].setText(tr('Back'))
        self['green'].setText(tr('Restore backup' if self.browsing else 'Create backup'))
        self['yellow'].setText(tr('Storage location'))
        self['blue'].setText(tr('Select projects' if self.browsing else 'Restore backup'))
        self.paths=backup.inventory(self.directory()) if self.browsing and self.directory() else []
        items=[(path,path.name[14:-5]) for path in self.paths] if self.browsing else [
            (name,('✓  ' if name in self.selected else '○  ')+name) for name in backup.PRODUCTS]
        sx,sy=self.width/1920,self.height/1080
        self['list'].l.setList([[key,self.api['MultiContentEntryText'](
            pos=(round(16*sx),round(10*sy)),size=(round(620*sx),round(54*sy)),font=0,text=label)]
            for key,label in items])
        if items:self['list'].moveToIndex(min(index,len(items)-1))
        self.describe()

    def describe(self):
        tr=self.tr
        self.preview=None
        self['result_title'].setText(tr('Restore backup' if self.browsing else 'Create backup'))
        self['result_status'].setText('')
        rows=[tr('Storage location'),str(self.directory() or '—'),'']
        if self.browsing:
            row=self['list'].getCurrent()
            if row:
                try:
                    payload=backup.load(row[0])
                    self.preview=row[0]
                    rows.extend((payload['created'],'SHA-256 · OK',''))
                    changes,radio,skipped,_=backup.plan(self.api['config'],payload,self.selected)
                    for name in backup.PRODUCTS:
                        if name in payload['projects']:
                            count=sum(c[0]==name for c in changes)+(len(radio) if name=='Warder Radio' else 0)
                            rows.append('%s  ·  %d / %d'%(name,count,len(payload['projects'][name])))
                            if skipped.get(name):rows.append('    '+tr('Unavailable')+'  %d'%skipped[name])
                    rows.extend(('',tr('Restore selected compatible settings only.')))
                except (OSError,ValueError,TypeError,RecursionError):rows.append(tr('Invalid backup'))
            else:rows.append(tr('No backups'))
        else:
            data=self.snapshot
            for name in backup.PRODUCTS:
                rows.append(('✓  ' if name in self.selected else '○  ')+name+'  ·  '+str(len(data.get(name,{})) if name in self.selected else 0))
            rows.extend(('',tr('Portable settings only. Passwords and tokens are excluded.'),
                         tr('Open each installed plugin once before backup or restore.')))
        self['descriptions'].setText('\n'.join(rows))

    def select(self):
        row=self['list'].getCurrent()
        if not row or self.browsing:return
        index=backup.PRODUCTS.index(row[0])
        if row[0] in self.selected:self.selected.remove(row[0])
        else:self.selected.add(row[0])
        self.render(index)

    def destination(self):
        if self.locations:
            self.location=(self.location+1)%len(self.locations)
        self.render()

    def browse(self):
        self.browsing=not self.browsing
        self.refresh()

    def execute(self):
        if self.browsing:
            if self.preview is None:return
            from Screens.MessageBox import MessageBox
            path=self.preview
            selected=tuple(self.selected)
            def confirmed(answer):
                if not answer:return
                try:
                    from Components.config import configfile
                    count,skipped,rollback=backup.restore(self.api['config'],configfile,path,selected)
                    self.describe()
                    self['result_status'].setText('OK · %d'%count)
                    if rollback:self['descriptions'].setText(self['descriptions'].getText()+'\n\n'+self.tr('Restart GUI after restoring settings.')+'\n'+str(rollback))
                except (OSError,ValueError,TypeError,RuntimeError,AttributeError,RecursionError):
                    self['result_status'].setText(self.tr('Unavailable'))
            self.session.openWithCallback(confirmed,MessageBox,self.tr('Restore selected compatible settings only.'),
                                          type=MessageBox.TYPE_YESNO,default=False)
        else:
            try:
                path=backup.save(self.directory(),backup.snapshot(self.api['config'],self.selected))
                self.describe()
                self['result_status'].setText('SHA-256 · OK')
                self['descriptions'].setText(self['descriptions'].getText()+'\n\n'+str(path))
            except (OSError,ValueError,TypeError,RuntimeError,AttributeError,RecursionError):
                self['result_status'].setText(self.tr('Unavailable'))

    def back(self):
        if self.browsing:self.browse()
        else:self.close()
