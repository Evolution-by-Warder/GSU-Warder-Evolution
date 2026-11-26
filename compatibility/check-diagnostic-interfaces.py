"""Check native interfaces used by the diagnostic screens in a real Enigma2 checkout."""
import ast
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1])
paths={
    'Components/Sources/CanvasSource.py':('CanvasSource',{'clear':(), 'fill':('x','y','width','height','color'),'flush':()}),
    'Components/PluginComponent.py':('PluginComponent',{'getPluginsForMenu':('menuid',)}),
    'Screens/ScanSetup.py':('ScanSetup',{'startScan':('tlist','flags','feid')}),
    'Components/Renderer/Canvas.py':('Canvas',{'changed':()}),
}
for path,(cls,methods) in paths.items():
    node=next(n for n in ast.parse((root/'lib/python'/path).read_text()).body if isinstance(n,ast.ClassDef) and n.name==cls)
    definitions={n.name:[a.arg for a in n.args.args][1:] for n in node.body if isinstance(n,ast.FunctionDef)}
    for method,parameters in methods.items():
        assert method in definitions and list(parameters)==definitions[method][:len(parameters)],(path,method,parameters)
interface=(root/'lib/service/iservice.h').read_text()
assert all(key in interface for key in ('isTimeshiftActive','isTimeshiftEnabled'))
print('Verified OpenBH sources',subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip())
