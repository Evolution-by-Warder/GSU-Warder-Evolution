"""Main-menu right workspace for swap/tools; retains original data controllers."""
from copy import deepcopy
from types import FunctionType
from xml.etree import ElementTree as ET
from . import warder_main as main, warder_tools_ui as tools_ui
from .warder_oscam import HeaderArtwork, CLEAR, PANEL_GLASS


def prepare(skin,width,height):
    root=ET.fromstring(skin);sx,sy=width/1920,height/1080
    root.set('backgroundColor',CLEAR)
    def box(node,x,y,w,h):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)));node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
    def fill(x,y,w,h,color,z):
        node=ET.SubElement(root,'eLabel',backgroundColor=color,zPosition=str(z));box(node,x,y,w,h)
    decorations=[]
    for node in list(root):
        if node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND:root.remove(node);continue
        x,y=map(int,node.get('position','0,0').split(','));w,h=map(int,node.get('size','0,0').split(','))
        if node.tag=='eLabel' and y==round(180*sy) and h==round(800*sy):root.remove(node);continue
        if node.tag=='eLabel' and y==round(182*sy) and h==round(796*sy):root.remove(node);continue
        if node.tag=='eLabel' and x>=round(1137*sx) and 182*sy<=y<978*sy:
            name='right_decoration_'+str(len(decorations));decorations.append(name)
            node.tag='widget';node.set('name',name);node.set('zPosition','1')
        name=node.get('name','')
        if name in ('list','selection','info') or name.startswith('inline_ecm_'):
            node.set('backgroundColor',CLEAR);node.set('transparent','1')
    node=ET.SubElement(root,'widget',name='right_header_art',zPosition='0');box(node,0,0,1920,164)
    for bounds in ((0,164,1920,16),(0,180,55,800),(1105,180,30,800),(1865,180,55,800),(0,980,1920,100)):
        fill(*bounds,main.BASE,0)
    for side,x,w in (('left',55,1050),('right',1135,730)):
        for bounds in ((x,180,w,2),(x,978,w,2),(x,182,2,796),(x+w-2,182,2,796)):fill(*bounds,main.CYAN,1)
        fill(x+2,182,w-4,796,PANEL_GLASS,1)
        node=ET.SubElement(root,'widget',name='right_opaque_'+side,backgroundColor=main.PANEL,zPosition='1');box(node,x+2,182,w-4,796)
    for name,bounds,font in (('title',(1160,200,680,45),28),('list',(1155,265,690,410),23),('config',(1155,265,690,540),22),('text',(1160,700,680,255),23),('scroll',(1160,265,680,680),23)):
        node=ET.SubElement(root,'widget',name='right_'+name,font='Regular;%d'%round(font*sy),backgroundColor=CLEAR,transparent='1',foregroundColor=main.CYAN if name=='title' else '#00ffffff',zPosition='6',scrollbarMode='showOnDemand')
        if name in ('list','config'):
            node.set('backgroundColorSelected',main.SELECTION);node.set('foregroundColorSelected','#00ffffff');node.set('itemHeight',str(round(42*sy)))
        box(node,*bounds)
    return ET.tostring(root,encoding='unicode'),decorations


class Session:
    def __init__(self,owner):self.owner=owner
    def __getattr__(self,name):return getattr(self.owner.screen.session,name)
    def open(self,target,*args,**kwargs):return self.openWithCallback(None,target,*args,**kwargs)
    def openWithCallback(self,callback,target,*args,**kwargs):
        owner=self.owner
        if target in owner.targets:return owner.enter(owner.targets[target],args,child=True)
        if callback:return owner.screen.session.openWithCallback(callback,target,*args,**kwargs)
        return owner.screen.session.open(target,*args,**kwargs)


class Workspace:
    def __init__(self,screen,api):
        self.screen,self.api=screen,api;self.model=None;self.kind=None;self.history=[];self.closed=False;self.focus_right=True
        self.targets={api['swap_manager']:'swap',api['SwapCreate']:'create',tools_ui.ToolsScreen:'tools',tools_ui.DiagnosticScreen:'diagnostic'}
        size=api['getDesktop'](0).size();self.sx,self.sy=size.width()/1920,size.height()/1080
        screen.skin,deco=prepare(screen.skin,size.width(),size.height())
        screen['right_header_art']=HeaderArtwork(size.width(),size.height())
        self.backings=[api['Label']('') for _ in range(2)]
        for name,widget in zip(('left','right'),self.backings):screen['right_opaque_'+name]=widget
        self.decorations=[]
        for name in deco:screen[name]=api['Label']('');self.decorations.append(screen[name])
        screen['right_title']=api['Label']('');screen['right_text']=api['Label']('')
        screen['right_list']=api['ListboxSys2']([]);screen['right_config']=api['ConfigList']([])
        screen['right_scroll']=api['ScrollLabel']('')
        self.widgets=[screen['right_'+n] for n in ('title','text','list','config','scroll')]
        for widget in self.widgets:widget.hide()
        screen['right_actions']=api['ActionMap'](['DirectionActions','SetupActions','ColorActions','WizardActions'],{'left':self.left,'right':self.right,'up':self.up,'down':self.down,'ok':self.choose,'green':self.green,'yellow':self.yellow,'red':self.back,'cancel':self.back,'back':self.back},-12)
        screen.onHide.append(self.suspend);screen.onClose.append(self.shutdown)
    @property
    def active(self):return self.model is not None
    def glass(self,enabled):
        for widget in self.backings+self.decorations:(widget.hide if enabled else widget.show)()
    def pigs(self):return self.screen._inline_ecm.pigs()
    def preview(self,visible,restore=True):
        for pig in self.pigs():
            if visible:
                if pig.instance is not None:pig.instance.show()
                if restore:pig.onShow()
            else:
                pig.onHide()
                if pig.instance is not None:pig.instance.hide()
        for name in ('selection','info'):(self.screen[name].show if visible else self.screen[name].hide)()
    def enter(self,kind,args=(),child=False):
        if self.closed:return
        if self.screen._inline_ecm.active:self.screen._inline_ecm.hide(restore_video=False)
        if self.active:
            if getattr(self.model,'_swap_busy',False):return
            if child:self.history.append((self.kind,self.model))
            else:self.dispose(self.model);self.history.clear()
        else:
            self.saved_footer={name:self.screen[name].getText() for name in ('red','green','yellow')}
            self.preview(False)
        target=next(cls for cls,k in self.targets.items() if k==kind)
        namespace=dict(self.api);methods={}
        # Narrow table columns to the right panel without changing swap data.
        def entry(**values):
            data=dict(values);x,y=data.get('pos',(0,0));w,h=data.get('size',(0,0));scale=690*self.sx/self.api['fhd'](730)
            if kind=='swap':data['pos']=(round(x*scale),y);data['size']=(min(round(w*scale),max(1,round(680*self.sx)-round(x*scale))),h)
            return self.api['MultiContentEntryText'](**data)
        namespace['MultiContentEntryText']=entry
        for name,value in vars(target).items():
            if isinstance(value,FunctionType):
                globals_=dict(value.__globals__);globals_.update(namespace)
                fn=FunctionType(value.__code__,globals_,name,value.__defaults__,value.__closure__);fn.__kwdefaults__=value.__kwdefaults__;methods[name]=fn
        methods['close']=lambda model,*values:self.leave()
        methods['setTitle']=lambda model,title:self.screen['right_title'].setText(title)
        model=type('Right_'+kind,(target,),methods)(Session(self),*(args if args else ((self.api,) if kind=='tools' else ())))
        self.model,self.kind=model,kind
        self.bind(model);self.glass(True);self.focus_right=True;self.focus()
        for fn in model.onLayoutFinish:fn()
        self.footer()
    def bind(self,model):
        for widget in self.widgets:widget.hide()
        self.screen['right_title'].show()
        for component in model.values():
            if isinstance(component,self.api['ActionMap']):component.setEnabled(False)
        for source,target in (('list','list'),('config','config'),('descriptions','text'),('file_info','scroll')):
            if source not in model:continue
            old=model[source];widget=self.screen['right_'+target]
            if source in ('list','config'):
                widget.onSelectionChanged[:]=[]
                if source=='config':widget.list=old.list
                else:widget.l.setList(old.list)
                widget.onSelectionChanged[:]=old.onSelectionChanged[:]
            else:widget.setText(old.getText())
            model[source]=widget;widget.show()
        self.screen['right_list'].l.setFont(0,self.api['gFont']('Regular',round(22*self.sy)))
        self.screen['right_list'].l.setItemHeight(round(40*self.sy))
    def footer(self):
        if not self.active:return
        for name in ('red','green','yellow'):
            self.screen[name].setText(main.text(self.api,'Back') if name=='red' else (self.model[name].getText() if name in self.model else ''))
    def focus(self):
        self.screen['list'].selectionEnabled(int(not self.focus_right))
        if self.active:
            for name in ('list','config'):
                if name in self.model:self.model[name].selectionEnabled(int(self.focus_right))
    def left(self):
        if not self.active:return 0
        self.focus_right=False;self.focus();return 1
    def right(self):
        if not self.active:return 0
        self.focus_right=True;self.focus();return 1
    def up(self):return self.move(-1)
    def down(self):return self.move(1)
    def move(self,direction):
        if not self.active:return 0
        if not self.focus_right:widget=self.screen['list']
        elif 'file_info' in self.model:
            (self.model['file_info'].pageUp if direction<0 else self.model['file_info'].pageDown)();return 1
        elif 'config' in self.model:
            widget=self.model['config']
            if widget.list:widget.setCurrentIndex((widget.getCurrentIndex()+direction)%len(widget.list))
            return 1
        else:widget=self.model['list']
        if widget.instance is not None:widget.instance.moveSelection(widget.instance.moveUp if direction<0 else widget.instance.moveDown)
        return 1
    def choose(self):
        if not self.active:return 0
        if not self.focus_right:
            if not getattr(self.model,'_swap_busy',False):self.screen.selectedmenuitem()
            return 1
        if self.kind=='create':
            current=self.model['config'].getCurrent()
            if current:
                setting=current[1];raw=getattr(setting,'choices',None)
                if raw is not None:
                    choices=getattr(raw,'choices',raw);items=[(str(v[1]),v[0]) if isinstance(v,(tuple,list)) else (str(v),v) for v in choices]
                    def selected(answer):
                        if answer and self.active and self.kind=='create':setting.value=answer[1];self.model['config'].invalidateCurrent()
                    self.screen.session.openWithCallback(selected,self.api['ChoiceBox'],title=str(current[0]),list=items)
                else:self.model['config'].handleKey(self.api['KEY_RIGHT'])
            return 1
        return self.action('ok')
    def action(self,name):
        actions=self.model['actions'].actions
        if name in actions:actions[name]()
        self.footer();return 1
    def green(self):
        if not self.active:return 0
        if not self.focus_right:
            if not getattr(self.model,'_swap_busy',False):self.screen.selectedmenuitem()
            return 1
        return self.action('green')
    def yellow(self):
        if not self.active:return 0
        return self.action('yellow')
    def dispose(self,model):
        for fn in model.onClose:fn()
    def back(self):
        if not self.active:return 0
        if getattr(self.model,'_swap_busy',False):return 1
        self.leave();return 1
    def leave(self,restore=True):
        if not self.active:return
        self.dispose(self.model)
        if self.history and restore:
            self.kind,self.model=self.history.pop();self.bind(self.model)
            for fn in self.model.onLayoutFinish:fn()
            self.footer();return
        for _,model in self.history:self.dispose(model)
        self.history.clear();self.model=None;self.kind=None
        for widget in self.widgets:widget.hide()
        for name,value in self.saved_footer.items():self.screen[name].setText(value)
        self.glass(False);self.preview(True,restore);self.screen['list'].selectionEnabled(1)
    def suspend(self):self.leave(restore=False)
    def shutdown(self):self.closed=True;self.suspend()


def install(screen,api):
    if api['getDesktop'](0).size().width()>=1280:screen._rightpane=Workspace(screen,api)


def show(screen,api,kind):
    if hasattr(screen,'_rightpane'):return screen._rightpane.enter(kind)
    if kind=='swap':return screen.session.open(api['swap_manager'])
    return tools_ui.open_tools(screen.session,api)
