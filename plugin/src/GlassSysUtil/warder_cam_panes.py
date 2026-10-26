"""Reuse CAM catalogue/removal/start controllers inside the manager's left pane."""
from types import FunctionType
from twisted.internet.threads import deferToThread
from . import warder_main as main


class Session:
    def __init__(self,owner,actual):self.owner,self.actual=owner,actual
    def __getattr__(self,name):return getattr(self.actual,name)
    def open(self,target,*args,**kwargs):return self.openWithCallback(None,target,*args,**kwargs)
    def openWithCallback(self,callback,target,*args,**kwargs):
        owner=self.owner
        if target is owner.api['ChoiceBox']:
            return owner.choices(kwargs.get('title',''),kwargs.get('list',[]),callback)
        if target is owner.api['InputBox'] and getattr(callback,'__name__','')=='setNewDelay':
            current=owner.api['config'].plugins.GlassSysUtil.par48.value
            return owner.choices(kwargs.get('title',''),[(str(n)+' s',str(n)) for n in range(1,31)],lambda answer:callback(answer[1] if answer else None),current=str(current))
        if target in owner.targets:
            return owner.open(target,args,callback)
        return self.actual.openWithCallback(callback,target,*args,**kwargs) if callback else self.actual.open(target,*args,**kwargs)


class Panes:
    def __init__(self,screen,api):
        from .native_start_config_ui import NativeStartConfigScreen
        self.screen,self.api=screen,api;self.model=None;self.kind=None;self.choice=None;self.closed=False;self.generation=0
        self.targets={api['ftp_center']:'download',api['ipk_uninstall_center']:'remove',NativeStartConfigScreen:'config'}
        self.actual_session=screen.session;self.session=Session(self,self.actual_session);screen.session=self.session
        screen['workspace_list']=api['ListboxSys2']([])
        screen['workspace_config']=api['ConfigList']([])
        for name in ('workspace_title','workspace_hint'):screen[name]=api['Label']('')
        self.widgets=[screen[n] for n in ('workspace_list','workspace_config','workspace_title','workspace_hint')]
        self.base=[screen[n] for n,bounds in screen._warder_cam_slots.items() if bounds[0]<1105 and n in screen]+[screen['cam_title']]
        for widget in self.widgets:widget.hide()
        self.base_visibility=[]
        for widget in self.base:
            state={'visible':widget.visible,'show':widget.show,'hide':widget.hide}
            def show(state=state):
                state['visible']=True
                if not self.active:state['show']()
            def hide(state=state):
                state['visible']=False;state['hide']()
            widget.show,widget.hide=show,hide
            self.base_visibility.append(state)
        screen.onClose.append(self.shutdown)
    def hide_base(self):
        for state in self.base_visibility:state['hide']()
    def restore_base(self):
        for state in self.base_visibility:
            state['show' if state['visible'] else 'hide']()
    @property
    def active(self):return self.model is not None or self.choice is not None
    def open(self,target,args,callback):
        if self.closed:return
        if self.active:
            if getattr(self.model,'saving',False):return
            self.leave(refresh=False)
        self.generation+=1;kind=self.targets[target];overlay=dict(self.api);methods={}
        for name,value in vars(target).items():
            if isinstance(value,FunctionType):
                namespace=dict(value.__globals__);namespace.update(overlay)
                fn=FunctionType(value.__code__,namespace,name,value.__defaults__,value.__closure__)
                fn.__kwdefaults__=value.__kwdefaults__;methods[name]=fn
        methods['setTitle']=lambda model,title:self.screen['workspace_title'].setText(title)
        methods['close']=lambda model,*values:self.leave(values=values)
        if kind=='remove':methods['updateList']=lambda model:self.load_installed(model,target)
        controller=type('EmbeddedCam_'+kind,(target,),methods)
        model=controller(self.session,*args)
        self.model,self.kind,self.callback=model,kind,callback
        for component in model.values():
            if isinstance(component,self.api['ActionMap']):component.setEnabled(False)
        name='config' if kind=='config' else 'list';old=model[name];widget=self.screen['workspace_'+name]
        if kind=='config':
            widget.list=old.list
            widget.onSelectionChanged[:]=old.onSelectionChanged[:]
        else:widget.l.setList([])
        model[name]=widget
        self.hide_base()
        for w in self.widgets:w.hide()
        widget.show();self.screen['workspace_title'].show();self.screen['workspace_hint'].show()
        self.old_footer={name:self.screen[name].getText() for name in ('red','green')}
        self.screen['red'].setText(main.text(self.api,'Back'))
        self.screen['green'].setText(main.text(self.api,'Save' if kind=='config' else 'Select with OK'))
        self.screen['workspace_hint'].setText(main.text(self.api,'Select with OK'))
        self.screen._warder_cam.focus(False)
        for fn in model.onLayoutFinish:fn()
        return model
    def load_installed(self,model,target):
        if self.closed or self.model is not model:return
        generation=self.generation
        self.screen['workspace_title'].setText(main.text(self.api,'Uninstall CAM/SRV menu'))
        pending=deferToThread(self.api['chckPckgList']);model.pending=pending
        def done(lines):
            if self.closed or self.model is not model or self.generation!=generation:return
            overlay=dict(self.api);overlay['chckPckgList']=lambda:lines
            fn=FunctionType(target.updateList.__code__,overlay,'updateList',target.updateList.__defaults__,target.updateList.__closure__)
            fn(model)
        def failed(failure):
            if not self.closed and self.model is model:self.screen['workspace_hint'].setText(main.text(self.api,'Unable to set up or read package feeds.'))
            return None
        pending.addCallback(done);pending.addErrback(failed)
    def move(self,direction):
        widget=self.screen['workspace_config' if self.kind=='config' else 'workspace_list']
        if self.choice is not None:widget=self.screen['workspace_list']
        if self.kind=='config' and self.choice is None:
            if widget.list:widget.setCurrentIndex((widget.getCurrentIndex()+direction)%len(widget.list))
        elif widget.instance is not None:
            widget.instance.moveSelection(widget.instance.moveUp if direction<0 else widget.instance.moveDown)
        return 1
    def focus(self,menu):
        if not self.active:return
        self.screen['workspace_config' if self.kind=='config' and self.choice is None else 'workspace_list'].selectionEnabled(int(not menu))
    def choose(self):
        if not self.active:return 1
        if self.choice is not None:
            current=self.screen['workspace_list'].getCurrent()
            if current:self.close_choice(current[0])
            return 1
        if self.kind=='download':self.model.doSelection()
        elif self.kind=='remove':
            if self.model['list'].getCurrent():self.model.selectedmenuitem()
        else:self.edit()
        return 1
    def edit(self):
        model=self.model
        if getattr(model,'saving',False):return
        current=model['config'].getCurrent()
        if not current:return
        setting=current[1]
        if setting in [v for k,v in model.settings.items() if k.endswith('_dir')]:model.choose();return
        if type(setting.value) is bool:
            setting.value=not setting.value;model['config'].invalidateCurrent();return
        raw=getattr(setting,'choices',None)
        if raw is not None:
            values=getattr(raw,'choices',raw)
            choices=[(str(v[1]),v[0]) if isinstance(v,(tuple,list)) else (str(v),v) for v in values]
            self.session.openWithCallback(lambda answer:self.changed(model,setting,answer[1] if answer else None),self.api['ChoiceBox'],title=str(current[0]),list=choices)
        else:
            number=type(setting.value) is int
            def changed(value):
                if value is None:return
                if number:
                    try:value=int(value)
                    except ValueError:return
                    limits=getattr(setting,'limits',None)
                    if limits and not limits[0][0]<=value<=limits[0][1]:return
                self.changed(model,setting,value)
            self.session.openWithCallback(changed,self.api['InputBox'],title=str(current[0]),text=str(setting.value),type=self.api['Input'].NUMBER if number else self.api['Input'].TEXT)
    def changed(self,model,setting,value):
        if value is not None and self.model is model and not self.closed:
            setting.value=value;model['config'].invalidateCurrent()
    def green(self):
        if self.choice is not None:return self.choose()
        if self.kind=='config':self.model.save();return 1
        return self.choose()
    def back(self):
        if self.choice is not None:self.close_choice(None);return 1
        if self.kind=='config':self.model.cancel()
        else:self.leave()
        return 1
    def leave(self,refresh=True,values=()):
        if self.choice is not None:self.close_choice(None)
        model=self.model
        if model is None:return
        self.generation+=1;self.model=None;self.kind=None
        for fn in model.onClose:fn()
        for widget in self.widgets:widget.hide()
        for name,text in self.old_footer.items():self.screen[name].setText(text)
        self.restore_base()
        if not self.closed:
            if refresh and self.callback:self.callback(*values)
            self.screen._warder_cam.focus(True)
    def choices(self,title,values,callback,current=None):
        if self.closed or self.choice is not None:return
        underlying=self.model is not None
        self.choice=(callback,underlying,self.screen['workspace_title'].getText())
        if not underlying:
            self.old_footer={name:self.screen[name].getText() for name in ('red','green')}
            self.hide_base()
        for widget in self.widgets:widget.hide()
        api=self.api;rows=[];index=0
        for n,pair in enumerate(values):
            if len(pair)<2:continue
            if pair[1]==current:index=n
            rows.append([pair,api['MultiContentEntryText'](pos=(api['fhd'](12),0),size=(api['fhd'](980),api['fhd'](36)),font=0,text=str(pair[0]))])
        self.screen['workspace_list'].l.setList(rows)
        self.screen['workspace_list'].moveToIndex(index)
        for name in ('workspace_list','workspace_title','workspace_hint'):self.screen[name].show()
        self.screen['workspace_title'].setText(title)
        self.screen['red'].setText(main.text(api,'Back'));self.screen['green'].setText(main.text(api,'Select with OK'))
        self.screen._warder_cam.focus(False)
    def close_choice(self,answer):
        callback,underlying,title=self.choice;self.choice=None
        if underlying:
            self.screen['workspace_list'].hide();self.screen['workspace_config'].show()
            self.screen['workspace_title'].setText(title);self.screen['green'].setText(main.text(self.api,'Save'))
        else:
            for widget in self.widgets:widget.hide()
            self.restore_base()
            for name,text in self.old_footer.items():self.screen[name].setText(text)
            if not self.closed:self.screen._warder_cam.focus(True)
        if callback and not self.closed:callback(answer)
    def shutdown(self):
        self.closed=True;self.leave(refresh=False)
