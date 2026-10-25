"""Retire GSU AutoInstall and cron UI without modifying image services/tasks."""
import ast

RETIRED = {'autoInstallMain', 'autoInstallMngMain', 'autoInstStatus', 'cronMng', 'SetupCronConf'}


def remove_autoinstall_cron(source):
    source = source.replace('from Components.Console import Console as CompConsole\n', '')
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    changes = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in RETIRED:
            changes.append((node.lineno - 1, node.end_lineno, ''))
        elif isinstance(node, ast.FunctionDef) and node.name == 'fill':
            changes.append((node.lineno - 1, node.end_lineno, ''))
        elif isinstance(node, ast.Assign) and any(ast.unparse(t) == 'autoInstallMng' for t in node.targets):
            changes.append((node.lineno - 1, node.end_lineno, ''))
        elif isinstance(node, ast.FunctionDef) and node.name == 'sessionAutostart':
            for statement in ast.walk(node):
                if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call) and ast.unparse(statement.value.func) == 'autoInstallMng.autoInstallStart':
                    changes.append((statement.lineno - 1, statement.end_lineno, ''))
        elif isinstance(node, ast.ClassDef) and node.name == 'SysUtilMngMain':
            for method in node.body:
                if not isinstance(method, ast.FunctionDef):
                    continue
                if method.name == '__init__':
                    for statement in ast.walk(method):
                        if isinstance(statement, ast.Assign) and any(ast.unparse(t) == 'self.menuListAll' for t in statement.targets):
                            for item in statement.value.elts:
                                if isinstance(item, ast.Tuple) and item.elts[0].value in ('12', '13'):
                                    changes.append((item.lineno - 1, item.end_lineno, ''))
                elif method.name == 'selectedmenuitem':
                    for statement in ast.walk(method):
                        if isinstance(statement, ast.If) and ast.unparse(statement.test) in ("selectedItem == '12'", "selectedItem == '13'"):
                            changes.append((statement.lineno - 1, statement.body[-1].end_lineno, ''))
                elif method.name == 'updatemenulist':
                    for statement in method.body:
                        if isinstance(statement, ast.For):
                            condition = next(n for n in statement.body if isinstance(n, ast.If))
                            expression = ast.unparse(condition.test)
                            expression = expression.replace("not os.path.exists('/etc/init.d/busybox-cron') and x[0] == '13' or ", '')
                            expression = expression.replace("x[0] in ['7', '13']", "x[0] == '7'")
                            changes.append((condition.lineno - 1, condition.lineno,
                                            '            if ' + expression + ':\n'))
    for start, end, text in sorted(changes, reverse=True):
        lines[start:end] = [text]
    result = ''.join(lines)
    compile(result, 'plugin.py', 'exec')
    return result
