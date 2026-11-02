#!/usr/bin/env python3
"""Check label wrap calls against the selected image's actual C++ eLabel API."""
import argparse
import ast
from pathlib import Path
import re
p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);args=p.parse_args()
header=(args.upstream.parent/'gui/elabel.h').read_text()
methods=set(re.findall(r'\b(setWrap|setNoWrap)\s*\(',header))
root=Path(__file__).resolve().parents[1]/'plugin/src/GlassSysUtil'
errors=[];checked=0
for path in root.glob('*.py'):
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr in ('setWrap','setNoWrap'):
            checked+=1
            if node.func.attr not in methods:errors.append('%s:%d eLabel.%s is absent'%(path.name,node.lineno,node.func.attr))
if errors:raise SystemExit('\n'.join(errors))
print('Native eLabel API: %d wrap calls verified'%checked)
