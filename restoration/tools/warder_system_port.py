"""Apply the Warder presentation to the existing system screen only."""
def port_warder_system(source):
    if 'import warder_system as _warder_system' in source:return source
    source='from Plugins.Extensions.GlassSysUtil import warder_system as _warder_system\n'+source
    start=source.index('class GlassSysInfoBrowser(');end=source.index('\nclass ',start+10)
    block=source[start:end].replace('        self.skin = GlassSysInfo', '        desktop = getDesktop(0).size()\n        self.skin = _warder_system.system_skin(GlassSysInfo, desktop.width(), desktop.height())').replace('        self.onLayoutFinish.append(self.LetsgoParty)', '        _warder_system.install(self, globals())\n        self.onLayoutFinish.append(self.LetsgoParty)')
    return source[:start]+block+source[end:]
