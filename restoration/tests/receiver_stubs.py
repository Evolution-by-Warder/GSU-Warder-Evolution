"""Small native API doubles. They never emulate receiver hardware or mutations."""
import builtins
import importlib.abc
import importlib.util
import pathlib
import sys
import types


class Component:
    TEXT=0;PASSWORD=1;NUMBER=2
    def __init__(self,*args,**kwargs):
        self.text=args[0] if args else ''
        self.instance=self;self.onSelectionChanged=[];self.list=[]
        self.callback=[];self.timeout=self;self.dataAvail=[];self.appClosed=[]
        self.l=self;self.index=0;self.visible=True
    def setText(self,value):self.text=value
    def getText(self):return self.text
    def setList(self,value):self.list=value
    def getCurrent(self):return self.list[self.index] if self.list else None
    def getSelectedIndex(self):return self.index
    def moveToIndex(self,index):self.index=index
    def getCurrentIndex(self):return self.index
    def setFont(self,*a):pass
    def setItemHeight(self,*a):pass
    def setWrapAround(self,*a):pass
    def selectionEnabled(self,*a):pass
    def connect(self,callback):self.callback.append(callback);return callback
    def show(self):self.visible=True
    def hide(self):self.visible=False
    def position(self):return self.__dict__.get('_position',types.SimpleNamespace(x=lambda:0,y=lambda:0))
    def move(self,value):self._position=value
    def resize(self,value):self._size=value
    def __getattr__(self,name):return lambda *a,**kw:None


class MenuList(Component):
    def __init__(self,values,*args,**kwargs):
        super().__init__();self.list=values


class Screen(dict):
    def __init__(self,session,*args,**kwargs):
        dict.__init__(self);self.session=session
        self.onLayoutFinish=[];self.onShown=[];self.onHide=[];self.onClose=[]
        self.onExecBegin=[];self.onExecEnd=[]
    def setTitle(self,title):self.title=title
    def close(self,*args):self.result=args


class Actions(Component):
    def __init__(self,contexts,actions,*args,**kwargs):
        super().__init__();assert all(isinstance(c,str) for c in contexts)
        self.contexts,self.actions=contexts,actions


class ConfigSection:
    def save(self):pass


class Setting:
    def __init__(self,default=None,choices=None,*args,**kwargs):
        self.value=default if default is not None else (choices[0][0] if choices else '')
        self.choices=choices
    def getValue(self):return self.value
    def setValue(self,value):self.value=value
    def save(self):pass
    def cancel(self):pass


class ConfigListScreen:
    def __init__(self,values,*args,**kwargs):
        self['config']=MenuList(values)
        self.onChangedEntry=[]
    def keyLeft(self):pass
    def keyRight(self):pass


class APIType(Component):
    @classmethod
    def getInstance(cls):return Component()


class APIModule(types.ModuleType):
    def __getattr__(self,name):
        if name.startswith('__'):raise AttributeError(name)
        value=type(name,(APIType,),{})
        setattr(self,name,value)
        return value


class Finder(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def find_spec(self,name,path=None,target=None):
        if name.startswith('Plugins.Extensions.GlassSysUtil'):
            return None
        if name.split('.')[0] in ('Plugins','Components','Screens','Tools','enigma','skin','ServiceReference','twisted'):
            return importlib.util.spec_from_loader(name,self,is_package=True)
    def create_module(self,spec):return APIModule(spec.name)
    def exec_module(self,module):
        module.__all__=[]
        name=module.__name__
        if name=='Components.config':
            module.config=types.SimpleNamespace(plugins=ConfigSection(),osd=types.SimpleNamespace(language=Setting('sk_SK')))
            module.configfile=types.SimpleNamespace(save=lambda:None)
            fields=('ConfigYesNo','ConfigInteger','ConfigText','ConfigDirectory','ConfigSelection','ConfigIP','ConfigPassword','ConfigNothing','ConfigSlider')
            for key in fields:setattr(module,key,Setting)
            module.ConfigSubsection=ConfigSection;module.NoSave=lambda x:x
            module.getConfigListEntry=lambda *args:args
            module.__all__=list(fields)+['config','configfile','ConfigSubsection','NoSave','getConfigListEntry']
        elif name=='Components.Pixmap':
            module.Pixmap=module.MovingPixmap=module.MultiPixmap=Component
            module.__all__=['Pixmap','MovingPixmap','MultiPixmap']
        elif name=='Components.ConfigList':
            module.ConfigListScreen=ConfigListScreen;module.ConfigList=MenuList
        elif name=='Components.MenuList':module.MenuList=MenuList
        elif name=='Screens.Screen':module.Screen=Screen
        elif name=='Components.ActionMap':
            module.ActionMap=module.HelpableActionMap=module.NumberActionMap=Actions
        elif name=='Components.Input':module.Input=Component
        elif name=='enigma':
            module.getDesktop=lambda i:types.SimpleNamespace(size=lambda:types.SimpleNamespace(width=lambda:1920,height=lambda:1080))
            module.addFont=lambda *a:None;module.gFont=lambda *a:a
            module.ePoint=lambda x,y:types.SimpleNamespace(x=lambda:x,y=lambda:y)
            module.eSize=lambda w,h:types.SimpleNamespace(width=lambda:w,height=lambda:h)
        elif name=='Tools.HardwareInfo':
            module.HardwareInfo=lambda:types.SimpleNamespace(get_device_name=lambda:'gbquad4kpro')
        elif name=='Tools.LoadPixmap':module.LoadPixmap=lambda *a,**kw:object()
        elif name=='Tools.Directories':
            module.fileExists=lambda path:pathlib.Path(path).exists()
            module.resolveFilename=lambda *a:'';module.SCOPE_CURRENT_SKIN=0
        elif name=='Components.MultiContent':
            module.MultiContentEntryText=lambda **kw:kw
            module.MultiContentEntryPixmapAlphaTest=lambda **kw:kw


def load(root):
    builtins._=lambda text:text
    finder=Finder();sys.meta_path.insert(0,finder)
    import Plugins.Extensions
    name='Plugins.Extensions.GlassSysUtil'
    module=types.ModuleType(name);module.__path__=[str(root)]
    sys.modules[name]=module
    spec=importlib.util.spec_from_file_location(name+'.plugin',root/'plugin.py')
    plugin=importlib.util.module_from_spec(spec);sys.modules[spec.name]=plugin
    spec.loader.exec_module(plugin)
    return plugin
