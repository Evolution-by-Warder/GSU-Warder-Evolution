"""Retain the client screen API/skin while replacing its obsolete HTML scraper."""
import ast


def port_oscam_clients(source):
    source = source.replace('from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox',
        'from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox\nfrom Plugins.Extensions.GlassSysUtil import oscam_clients_ui as _oscam_clients_ui', 1)
    tree = ast.parse(source)
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'oscam_Users')
    lines = source.splitlines(keepends=True)
    changes = []
    for method in cls.body:
        if not isinstance(method, ast.FunctionDef):
            continue
        if method.name == '__init__':
            body = ast.get_source_segment(source, method)
            body = body.replace("        self['blue_button'] = Label('')", "        self['blue_button'] = Label('')\n        _oscam_clients_ui.initialize(self)")
            body = body.replace('        self.onLayoutFinish.append(self.oscamUsers)',
                '        self.onLayoutFinish.append(self.prepareClients)\n        self.onLayoutFinish.append(self.oscamUsers)')
            # All five rows have placeholders before the first response too.
            body = body.replace("self['status_values_2'] = Label('..........\\n..........\\n..........')", "self['status_values_2'] = Label('..........\\n..........\\n..........\\n..........\\n..........')")
        elif method.name in ('oscamUsers', 'reactivate', 'chngState', 'exit'):
            call = {'oscamUsers': 'request(self, globals())', 'reactivate': 'details(self, globals())',
                    'chngState': 'change_state(self, globals())', 'exit': 'close(self)'}[method.name]
            body = 'def ' + method.name + '(self):\n        _oscam_clients_ui.' + call
        else:
            continue
        changes.append((method.lineno - 1, method.end_lineno, '    ' + body + '\n'))
    changes.append((cls.end_lineno, cls.end_lineno,
        '\n    def prepareClients(self):\n        _oscam_clients_ui.prepare(self)\n'))
    for start, end, body in sorted(changes, reverse=True):
        lines[start:end] = [body]
    result = ''.join(lines)
    compile(result, 'plugin.py', 'exec')
    return result
