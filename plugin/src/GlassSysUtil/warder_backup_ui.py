"""One Warder-styled local backup workspace; no network or implicit restore."""
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap
from xml.etree import ElementTree as ET
from twisted.internet.threads import deferToThread

from .warder_screen import Screen
from . import warder_dashboard as dashboard, warder_backup as backup
from .i18n import for_api
from .warder_menu_icons import pixmap_entry


def archive_title(path):
    from datetime import datetime
    try:
        stamp=datetime.strptime(path.name[14:29],'%Y%m%d-%H%M%S')
        return stamp.strftime('%d.%m.%Y  %H:%M:%S')+'  ·  '+path.stem[30:]
    except ValueError:return path.stem


def summary_lines(tr,summary,completed=False):
    labels=(tr('Restored' if completed else 'To restore'),tr('Unchanged'),tr('Incompatible'),tr('Not selected'))
    totals=tuple(sum(row[i] for row in summary.values()) for i in range(4))
    lines=['%s: %d'%(label,count) for label,count in zip(labels,totals)]
    lines.append('')
    for name,counts in summary.items():
        lines.append(name)
        lines.append('    '+'  ·  '.join('%s: %d'%(label,count) for label,count in zip(labels,counts) if count) if any(counts) else '    0')
    return lines


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
        self.last_archive=None
        self.preview=None
        self.preview_digest=None
        self.locked=None
        self.password=None
        self.busy=False
        self.closed=False
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
             'up':lambda:None if self.busy else self['list'].up(),'down':lambda:None if self.busy else self['list'].down(),
             'left':self['descriptions'].pageUp,'right':self['descriptions'].pageDown},-2)
        self.onLayoutFinish.append(self.refresh)
        self.onClose.append(self.cleanup)

    def tr(self,key):return for_api(self.api,key)

    def cleanup(self):
        self.closed=True
        self.password=None
        self.preview=None
        self.preview_digest=None

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
        items=[(path,archive_title(path)) for path in self.paths] if self.browsing else [
            (name,('✓  ' if name in self.selected else '○  ')+name) for name in backup.PRODUCTS]
        sx,sy=self.width/1920,self.height/1080
        rows=[]
        for key,label in items:
            icon=pixmap_entry(self.api,'project-backup' if self.browsing else key,
                (round(12*sx),round(8*sy)),(round((54 if self.browsing else 120)*sx),round(58*sy)),
                project=not self.browsing)
            left=(80 if self.browsing else 148) if icon is not None else 16
            row=[key,self.api['MultiContentEntryText'](pos=(round(left*sx),round(10*sy)),
                size=(round((624-left)*sx),round(54*sy)),font=0,text=label,
                color=0xffffff if self.browsing or key in self.selected else 0x8291a5)]
            if icon is not None:row.append(icon)
            rows.append(row)
        self['list'].l.setList(rows)
        if self.browsing and self.last_archive in self.paths:index=self.paths.index(self.last_archive)
        if items:self['list'].moveToIndex(min(index,len(items)-1))
        self.describe()

    def describe(self):
        tr=self.tr
        self.preview=None
        self.preview_digest=None
        self.locked=None
        self.password=None
        self['green'].setText(tr('Restore backup' if self.browsing else 'Create backup'))
        self['result_title'].setText(tr('Restore backup' if self.browsing else 'Create backup'))
        self['result_status'].setText('')
        rows=[tr('Storage location'),str(self.directory() or '—'),'']
        if self.browsing:
            row=self['list'].getCurrent()
            if row:
                self.last_archive=row[0]
                try:
                    if backup.file_kind(row[0])=='private':
                        self.locked=row[0]
                        rows.extend((tr('Private backup'),tr('Enter backup password') if backup.crypto.available() else tr('Private backup encryption unavailable')))
                        self['green'].setText(tr('Unlock backup') if backup.crypto.available() else '')
                    else:
                        payload=backup.load(row[0])
                        self.set_preview(row[0],payload)
                        return
                except (OSError,ValueError,TypeError,RecursionError):rows.append(tr('Invalid backup'))
            else:rows.append(tr('No backups'))
        else:
            data=self.snapshot
            for name in backup.PRODUCTS:
                rows.append(('✓  ' if name in self.selected else '○  ')+name+'  ·  '+str(len(data.get(name,{})) if name in self.selected else 0))
            rows.extend(('',tr('Standard backup'),tr('Portable settings only. Passwords and tokens are excluded.'),
                         tr('Private backup')+' · '+(tr('Ready') if backup.crypto.available() else tr('Unavailable')),
                         tr('Open each installed plugin once before backup or restore.')))
        self['descriptions'].setText('\n'.join(rows))

    def select(self):
        if self.busy or self.closed:return
        if self.browsing and self.locked is not None:self.unlock();return
        row=self['list'].getCurrent()
        if not row or self.browsing:return
        index=backup.PRODUCTS.index(row[0])
        if row[0] in self.selected:self.selected.remove(row[0])
        else:self.selected.add(row[0])
        self.render(index)

    def destination(self):
        if self.busy or self.closed:return
        if self.locations:
            self.location=(self.location+1)%len(self.locations)
        self.render()

    def browse(self):
        if self.busy or self.closed:return
        self.browsing=not self.browsing
        self.refresh()

    def set_preview(self,path,payload,password=None):
        tr=self.tr
        private=password is not None
        changes,radio,skipped,_=backup.plan(self.api['config'],payload,self.selected,private=private)
        rows=[tr('Storage location'),str(path.parent),'',payload['created'],
              ('AES-256-GCM' if private else 'SHA-256')+' · OK','']
        summary=backup.outcome(payload,self.selected,changes,radio,skipped)
        rows.extend(summary_lines(tr,summary))
        rows.extend(('',tr('Restore selected compatible settings only.')))
        self.preview=path
        self.preview_digest=backup.fingerprint(payload)
        self.locked=None
        self.password=password
        self['descriptions'].setText('\n'.join(rows))
        self['green'].setText(tr('Restore backup'))

    def task(self,work,done,failed):
        if self.busy or self.closed:return
        self.busy=True
        self['result_status'].setText(self.tr('Loading…'))
        def success(value):
            self.busy=False
            if not self.closed:done(value)
        def failure(_):
            self.busy=False
            if not self.closed:failed()
        try:deferToThread(work).addCallbacks(success,failure)
        except (OSError,RuntimeError,TypeError,AttributeError):failure(None)

    def ask_password(self,title,callback):
        from .warder_backup_password import BackupPassword
        self.session.openWithCallback(callback,BackupPassword,self.api,self.tr(title))

    def unlock(self):
        if self.busy or self.closed or self.locked is None:return
        if not backup.crypto.available():
            self['result_status'].setText(self.tr('Private backup encryption unavailable'))
            return
        path=self.locked
        def entered(password):
            if self.closed or not password or self.locked!=path:return
            def done(payload):
                if self.locked==path:
                    try:
                        self.set_preview(path,payload,password)
                        self['result_status'].setText('AES-256-GCM · OK')
                    except (OSError,ValueError,TypeError,RuntimeError,AttributeError,RecursionError):
                        self['result_status'].setText(self.tr('Invalid backup'))
            self.task(lambda:backup.load(path,password=password),done,
                      lambda:self['result_status'].setText(self.tr('Incorrect password or damaged backup')))
        self.ask_password('Enter backup password',entered)

    def create_mode(self):
        from .warder_dialog import choose
        choices=[(self.tr('Standard backup'),False)]
        if backup.crypto.available():choices.append((self.tr('Private backup'),True))
        if len(choices)==1:self.create()
        else:choose(self.session,self.api,self.mode_selected,self.tr('Create backup'),choices)

    def mode_selected(self,item):
        if self.closed or item is None:return
        if not item[1]:self.create();return
        def first(password):
            if not password or self.closed:return
            def second(confirmation):
                if not confirmation or self.closed:return
                if password!=confirmation:
                    self['result_status'].setText(self.tr('Passwords do not match'))
                    return
                self.create(password)
            self.ask_password('Confirm backup password',second)
        self.ask_password('Enter backup password',first)

    def create(self,password=None):
        if self.closed or self.busy:return
        try:
            directory=self.directory()
            if directory is None:raise ValueError('No storage')
            data=backup.snapshot(self.api['config'],self.selected,private=password is not None)
            if not data:raise ValueError('No settings')
        except (OSError,ValueError,TypeError,RuntimeError,AttributeError,RecursionError):
            self['result_status'].setText(self.tr('Unavailable'))
            return
        def done(path):
            self.describe()
            self['result_status'].setText(('AES-256-GCM' if password is not None else 'SHA-256')+' · OK')
            self['descriptions'].setText(self['descriptions'].getText()+'\n\n'+str(path))
        self.task(lambda:backup.save(directory,data,password=password),done,
                  lambda:self['result_status'].setText(self.tr('Unavailable')))

    def execute(self):
        if self.closed or self.busy:return
        if not self.browsing:
            self.create_mode()
            return
        if self.locked is not None:self.unlock();return
        if self.preview is None:return
        from Screens.MessageBox import MessageBox
        path=self.preview
        selected=tuple(self.selected)
        password=self.password
        digest=self.preview_digest
        def confirmed(answer):
            if self.closed:return
            if not answer:
                self.describe()
                return
            if self.preview!=path or self.preview_digest!=digest:return
            self.password=None
            try:
                from Components.config import configfile
                count,skipped,rollback,summary=backup.restore(self.api['config'],configfile,path,selected,
                    password=password,expected_digest=digest,details=True)
                self.describe()
                self['result_title'].setText(self.tr('Restore result'))
                self['result_status'].setText('OK · %d'%count)
                rows=summary_lines(self.tr,summary,completed=True)
                if rollback:rows.extend(('',self.tr('Restart GUI after restoring settings.'),
                                         self.tr('Backup before restore'),str(rollback)))
                self['descriptions'].setText('\n'.join(rows))
            except (OSError,ValueError,TypeError,RuntimeError,AttributeError,RecursionError):
                self.describe()
                self['result_status'].setText(self.tr('Unavailable'))
        self.session.openWithCallback(confirmed,MessageBox,self.tr('Restore selected compatible settings only.'),
                                      type=MessageBox.TYPE_YESNO,default=False)

    def back(self):
        if self.busy:return
        if self.browsing:self.browse()
        else:self.close()
