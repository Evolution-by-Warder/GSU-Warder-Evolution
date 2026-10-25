"""Replace original blocking swap mutations while preserving screen signatures."""
import ast


def port_swap(source):
    source = source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox',
        'from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil import swap_ui as _swap_ui', 1)
    lines = source.splitlines(keepends=True)
    changes = []
    for cls in ast.parse(source).body:
        if not isinstance(cls, ast.ClassDef) or cls.name not in ('swap_manager', 'SwapCreate'):
            continue
        for method in cls.body:
            if not isinstance(method, ast.FunctionDef):
                continue
            body = ast.get_source_segment(source, method)
            if method.name == '__init__':
                body = body.replace('        self.list = []', '        _swap_ui.init(self)\n        self.list = []', 1)
                body = body.replace('(self.close)', '(self.exitSwap)')
            elif cls.name == 'swap_manager' and method.name == 'add':
                body = 'def add(self):\n        if not self._swap_busy:\n            self.session.openWithCallback(self.readSwapInfo, SwapCreate)'
            elif method.name == 'swapDeleteQuestion':
                body = 'def swapDeleteQuestion(self):\n        _swap_ui.delete_question(self, globals())'
            elif cls.name == 'swap_manager' and method.name == 'readSwapInfo':
                body = 'def readSwapInfo(self, callback=None):\n        _swap_ui.read_info(self, globals())'
            elif method.name == 'swapDelete':
                body = 'def swapDelete(self, answer):\n        _swap_ui.delete(self, globals(), answer)'
            elif cls.name == 'SwapCreate' and method.name == 'mountDevices':
                body = "def mountDevices(self):\n        return [_('None')]"
            elif cls.name == 'SwapCreate' and method.name == 'SwapDefine':
                body = body.replace("        self.setTitle(_('Create'))", "        self.setTitle(_('Create'))\n        _swap_ui.load_places(self, globals())")
            elif cls.name == 'SwapCreate' and method.name == 'SwapCreate':
                body = 'def SwapCreate(self):\n        _swap_ui.create(self, globals())'
            else:
                continue
            changes.append((method.lineno - 1, method.end_lineno, '    ' + body + '\n'))
        changes.append((cls.end_lineno, cls.end_lineno,
            '\n    def exitSwap(self):\n        _swap_ui.exit_screen(self, globals())\n'))
    for start, end, text in sorted(changes, reverse=True):
        lines[start:end] = [text]
    result = ''.join(lines)
    compile(result, 'plugin.py', 'exec')
    return result
