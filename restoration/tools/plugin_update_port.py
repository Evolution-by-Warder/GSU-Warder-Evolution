"""Retire three main-menu tools and replace the obsolete FTP plugin updater."""
import ast


def port_plugin_update(source):
    tree=ast.parse(source);lines=source.splitlines(keepends=True);changes=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name=='main5':
            changes.append((node.lineno-1,node.end_lineno,'def main5(session, **kwargs):\n    return  # Retired Devices Manager shortcut.\n'))
        if isinstance(node,ast.FunctionDef) and node.name=='Plugins':
            for statement in ast.walk(node):
                if isinstance(statement,ast.If) and len(statement.body)==1 and 'fnc=main5' in ast.unparse(statement.body[0]):
                    changes.append((statement.lineno-1,statement.end_lineno,''))
        if isinstance(node,ast.ClassDef) and node.name=='cfgGsuScreen':
            for statement in ast.walk(node):
                if isinstance(statement,ast.Expr) and isinstance(statement.value,ast.Call) and 'getConfigListEntry' in ast.unparse(statement) and 'par55' in ast.unparse(statement):
                    changes.append((statement.lineno-1,statement.end_lineno,'            pass  # Retired Devices Manager shortcut option.\n'))
        if not isinstance(node,ast.ClassDef) or node.name!='SysUtilMngMain':continue
        for method in node.body:
            if not isinstance(method,ast.FunctionDef):continue
            if method.name=='__init__':
                for statement in ast.walk(method):
                    if isinstance(statement,ast.Dict):
                        for index,key in enumerate(statement.keys):
                            if isinstance(key,ast.Constant) and key.value=='blue':
                                statement.keys.pop(index);statement.values.pop(index)
                                # Replace the ActionMap assignment as a whole below.
                                assignment=next(n for n in ast.walk(method) if isinstance(n,ast.Assign) and any(child is statement for child in ast.walk(n)))
                                changes.append((assignment.lineno-1,assignment.end_lineno,'        '+ast.unparse(assignment)+'\n'))
                                break
                for statement in ast.walk(method):
                    if isinstance(statement,ast.Assign) and any(ast.unparse(t)=='self.menuListAll' for t in statement.targets):
                        kept=[ast.unparse(item) for item in statement.value.elts if item.elts[0].value not in ('11','14','15')]
                        kept.append("('16', _('Update'), _('Check for a new version of Glass System Utility Warder Evolution'))")
                        changes.append((statement.lineno-1,statement.end_lineno,'        self.menuListAll = [\n            '+',\n            '.join(kept)+']\n'))
                last=next(statement for statement in reversed(method.body) if isinstance(statement,ast.Return))
                changes.append((last.lineno-1,last.lineno-1,'        self._plugin_update = _StartupUpdateCheck(self, globals())\n'))
            elif method.name=='selectedmenuitem':
                for statement in ast.walk(method):
                    if isinstance(statement,ast.If) and ast.unparse(statement.test) in ("selectedItem == '11'","selectedItem == '14'","selectedItem == '15'"):
                        replacement="            elif selectedItem == '16':\n                self.updatechckact()\n" if ast.unparse(statement.test)=="selectedItem == '11'" else ''
                        changes.append((statement.lineno-1,statement.body[-1].end_lineno,replacement))
            elif method.name=='updatechckact':
                changes.append((method.lineno-1,method.end_lineno,'    def updatechckact(self):\n        self._plugin_update.request(manual=True)\n'))
            elif method.name in ('updAnswer','cmdAnsw','resetRootPass','_commandFinished'):
                signature=lines[method.lineno-1]
                changes.append((method.lineno-1,method.end_lineno,signature+'        return  # Retired legacy action.\n'))
    for start,end,replacement in sorted(changes,reverse=True):lines[start:end]=[replacement]
    result=''.join(lines)
    result='from Plugins.Extensions.GlassSysUtil.plugin_update_ui import StartupUpdateCheck as _StartupUpdateCheck\n'+result
    # New strings are absent from the original translation catalogue.
    result=result.replace("'16', _('Update'), _('Check for a new version of Glass System Utility Warder Evolution')", "'16', _plugin_update_text(globals(), 'Update'), _plugin_update_text(globals(), 'Check for a new version of Glass System Utility Warder Evolution')")
    result=result.replace('import StartupUpdateCheck as _StartupUpdateCheck','import StartupUpdateCheck as _StartupUpdateCheck, text as _plugin_update_text',1)
    compile(result,'plugin.py','exec')
    return result
