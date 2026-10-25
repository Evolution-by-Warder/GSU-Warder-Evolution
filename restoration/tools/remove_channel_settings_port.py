"""Remove the maintainer-retired channel archive importer, not just its menu row."""
import ast


def remove_channel_settings(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    changes = []
    for cls in tree.body:
        if not isinstance(cls, ast.ClassDef):
            continue
        if cls.name in ('settings_satxml', 'settings_center'):
            changes.append((cls.lineno - 1, cls.end_lineno, ''))
        elif cls.name == 'SysUtilMngMain':
            for method in cls.body:
                if not isinstance(method, ast.FunctionDef):
                    continue
                if method.name == '__init__':
                    for node in ast.walk(method):
                        if isinstance(node, ast.Assign) and any(ast.unparse(t) == 'self.menuListAll' for t in node.targets):
                            for item in node.value.elts:
                                if isinstance(item, ast.Tuple) and item.elts[0].value == '10':
                                    changes.append((item.lineno - 1, item.end_lineno, ''))
                elif method.name == 'selectedmenuitem':
                    for node in ast.walk(method):
                        if isinstance(node, ast.If) and ast.unparse(node.test) == "selectedItem == '10'":
                            changes.append((node.lineno - 1, node.body[-1].end_lineno, ''))
                elif method.name == 'reactivate':
                    # Retain stable dispatch IDs when a menu item is removed.
                    body = '''    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            entry = next((entry for entry in self.menuListAll if entry[0] == selection[0]), None)
            self['info'].setText(str(entry[2]) if entry else '')
'''
                    changes.append((method.lineno - 1, method.end_lineno, body))
    for start, end, text in sorted(changes, reverse=True):
        lines[start:end] = [text]
    result = ''.join(lines)
    compile(result, 'plugin.py', 'exec')
    return result
