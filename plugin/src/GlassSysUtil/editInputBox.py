from enigma import getPrevAsciiCode, getDesktop
from Screens.Screen import Screen
from Components.ActionMap import NumberActionMap
from Components.Label import Label
import os
from Components.Input import Input
from Tools.BoundFunction import boundFunction

class editInputBox(Screen):
    FHD = getDesktop(0).size().width()
    if FHD == 1920:
        skin = """<screen name="editInputBox" position="center,center" size="1800,160" title="InputBox">
                        <widget name="text" position="10,10" size="1770,90" font="Regular;25"/>
    <eLabel position="0,100" size="1800,2" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="input" position="10,120" size="1780,30" font="Regular;25"/>
                        </screen>"""
    elif FHD == 3840:
        skin = """<screen name="editInputBox" position="center,center" size="3600,320" title="InputBox">
                        <widget name="text" position="20,20" size="3540,180" font="Regular;50"/>
    <eLabel position="0,200" size="3600,4" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="input" position="20,240" size="3560,60" font="Regular;50"/>
                        </screen>"""
    else:
        skin = """<screen name="editInputBox" position="center,center" size="1200,110" title="InputBox">
                        <widget name="text" position="10,5" size="1180,60" font="Regular;17"/>
    <eLabel position="0,65" size="1200,1" backgroundColor="#888888" zPosition="5" transparent="0" />
                        <widget name="input" position="10,72" size="1180,24" font="Regular;17"/>
                        </screen>"""
    def __init__(self, session, title = "", windowTitle = _("Input"), useableChars = None, **kwargs):
        Screen.__init__(self, session)

        self["text"] = Label(title)
        self["input"] = Input(**kwargs)
        self.onShown.append(boundFunction(self.setTitle, windowTitle))
        if useableChars is not None:
            self["input"].setUseableChars(useableChars)

        self["actions"] = NumberActionMap(["WizardActions", "InputBoxActions", "InputAsciiActions", "KeyboardInputActions"], 
        {
            "gotAsciiCode": self.gotAsciiCode,
            "ok": self.go,
            "back": self.cancel,
            "left": self.keyLeft,
            "right": self.keyRight,
            "home": self.keyHome,
            "end": self.keyEnd,
            "deleteForward": self.keyDelete,
            "deleteBackward": self.keyBackspace,
            "tab": self.keyTab,
            "toggleOverwrite": self.keyInsert,
            "1": self.keyNumberGlobal,
            "2": self.keyNumberGlobal,
            "3": self.keyNumberGlobal,
            "4": self.keyNumberGlobal,
            "5": self.keyNumberGlobal,
            "6": self.keyNumberGlobal,
            "7": self.keyNumberGlobal,
            "8": self.keyNumberGlobal,
            "9": self.keyNumberGlobal,
            "0": self.keyNumberGlobal
        }, -1)

        if self["input"].type == Input.TEXT:
            self.onExecBegin.append(self.setKeyboardModeAscii)
        else:
            self.onExecBegin.append(self.setKeyboardModeNone)

    def gotAsciiCode(self):
        self["input"].handleAscii(getPrevAsciiCode())

    def keyLeft(self):
        self["input"].left()

    def keyRight(self):
        self["input"].right()

    def keyNumberGlobal(self, number):
        self["input"].number(number)

    def keyDelete(self):
        self["input"].delete()

    def go(self):
        self.close(self["input"].getText())

    def cancel(self):
        self.close(None)

    def keyHome(self):
        self["input"].home()

    def keyEnd(self):
        self["input"].end()

    def keyBackspace(self):
        self["input"].deleteBackward()

    def keyTab(self):
        self["input"].tab()

    def keyInsert(self):
        self["input"].toggleOverwrite()

