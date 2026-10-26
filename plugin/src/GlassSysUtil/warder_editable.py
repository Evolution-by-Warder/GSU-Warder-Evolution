"""Mark config values as editable without replacing their setting objects."""
from . import warder_main as main


def mark(model):
    if 'config' not in model:return
    if not hasattr(model,'_editable_marks'):model._editable_marks=[]
    for row in model['config'].list:
        if len(row)<2:continue
        setting=row[1]
        if any(item[0] is setting for item in model._editable_marks):continue
        original=getattr(setting,'getMulti',None)
        if not callable(original):continue
        def display(selected,original=original):
            value=original(selected)
            if value and value[0] in ('text','mtext'):
                return ('text',r'\c003ee8ff'+str(value[1])+' ✎'+r'\c00ffffff')
            return value
        setting.getMulti=display;model._editable_marks.append((setting,original,display))


def restore(model):
    for setting,original,display in getattr(model,'_editable_marks',[]):
        if setting.getMulti is display:setting.getMulti=original
    model._editable_marks=[]
