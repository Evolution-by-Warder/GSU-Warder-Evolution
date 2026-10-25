"""Move About to main-screen blue and keep the project name untranslated."""

def port_about_shortcut(source):
    source=source.replace("description=_('Glass System Utility')", "description=_warder_main.text(globals(), 'Receiver information, CAM/ECM and diagnostics')")
    source=source.replace("_('Glass System Utility')", '_warder_main.PLUGIN_NAME')
    start=source.index('class SysUtilMngMain(')
    end=source.index('\nclass GlassSysInfoBrowser',start)
    block=source[start:end]
    block=block.replace("'Diagnostic bundle and plugin information.'", "'Create one archive with system information and GSU logs.'")
    block=block.replace("self['blue'] = Label('')", "self['blue'] = Label(_warder_tools_ui.text(globals(), 'About plugin'))")
    block=block.replace("{'green': self.selectedmenuitem,", "{'blue': self.aboutPlugin, 'green': self.selectedmenuitem,")
    if '    def aboutPlugin(self):' not in block:
        block=block.replace('    def resetRootPass(self, a):', "    def aboutPlugin(self):\n        self.session.open(_warder_tools_ui.AboutScreen, globals())\n\n    def resetRootPass(self, a):")
    result=source[:start]+block+source[end:]
    compile(result,'plugin.py','exec')
    return result
