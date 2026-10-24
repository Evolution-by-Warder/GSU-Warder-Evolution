#!/usr/bin/env python3
"""Recover the unchanged 13.20 source from its oldest complete bytecode.

Run on Python 3.12 with uncompyle6==3.9.3, xdis==6.1.8 and
spark-parser==1.9.0. Input is the maintainer's immutable original IPK.
No original plugin code is executed. lib2to3 translates syntax only.
"""
import contextlib
import hashlib
import io
import json
import pathlib
import signal
import sys
import tarfile
import tempfile

ORIGINAL_SHA256 = '81aea6eb25b5ed519e904af87a3d7bece5d32ae6886a1690dac8ab47306fe3f7'


def members(ipk):
    raw = pathlib.Path(ipk).read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Input is not the approved GSU 13.20 original')
    offset = 8
    if raw[:8] != b'!<arch>\n':
        raise ValueError('Invalid original IPK')
    while offset + 60 <= len(raw):
        head = raw[offset:offset+60]
        size = int(head[48:58])
        name = head[:16].decode().strip().rstrip('/')
        data = raw[offset+60:offset+60+size]
        offset += 60 + size + size % 2
        if name.startswith('data.tar'):
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                for item in archive:
                    if item.isfile():
                        path = pathlib.PurePosixPath(item.name.removeprefix('./'))
                        if path.is_absolute() or '..' in path.parts:
                            raise ValueError('Invalid archive path')
                        yield str(path), archive.extractfile(item).read()


def inventory(code, prefix=''):
    result = []
    for nested in code.co_consts:
        if hasattr(nested, 'co_code'):
            name = prefix + nested.co_name
            result.append({'name': name, 'args': nested.co_argcount})
            result.extend(inventory(nested, name + '.'))
    return result


def recover(ipk, destination):
    from uncompyle6.main import decompile_file
    from uncompyle6.scanners.scanner26 import Scanner26
    from xdis.load import load_module
    from lib2to3.refactor import RefactoringTool, get_fixers_from_package
    # uncompyle6's 2.6 scanner stores a constant INDEX in ADD_VALUE.attr.
    # Its constant-list printer consumes the VALUE. Without this correction,
    # e.g. ActionMap contexts become [63, 64, 65, 66, 67] instead of strings.
    original = Scanner26.bound_collection_from_tokens
    def collections(self, *args, **kwargs):
        tokens = original(self, *args, **kwargs)
        if tokens:
            for token in tokens:
                if token.kind == 'ADD_VALUE':
                    token.attr = token.pattr
        return tokens
    Scanner26.bound_collection_from_tokens = collections
    payload = dict(members(ipk))
    root = 'usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/'
    with tempfile.TemporaryDirectory() as temporary:
        original_pyc = pathlib.Path(temporary)/'plugin26.pyc'
        original_pyc.write_bytes(payload[root+'plugin.pyo'])
        target_pyc = pathlib.Path(temporary)/'plugin312.pyc'
        target_pyc.write_bytes(payload[root+'plugin.py312o'])
        oldest = inventory(load_module(str(original_pyc))[3])
        latest = inventory(load_module(str(target_pyc))[3])
        assert oldest == latest, 'Original function inventory or signatures differ'
        source = io.StringIO()
        log = io.StringIO()
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            decompile_file(str(original_pyc), outstream=source, showgrammar={})
        recovered = source.getvalue()
        # A module's implicit RETURN_VALUE is not a source-level statement.
        assert recovered.rstrip().endswith('\nreturn')
        recovered = recovered.rstrip()[:-len('return')].rstrip()+'\n'
        if 'decompilation failed' in recovered or 'Unsupported opcode' in recovered:
            raise ValueError('Incomplete decompilation')
        tool = RefactoringTool(get_fixers_from_package('lib2to3.fixes'))
        converted = str(tool.refactor_string(recovered, 'plugin.py'))
        compile(converted, 'plugin.py', 'exec')
        destination = pathlib.Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(converted)
        record = {'original_ipk_sha256': ORIGINAL_SHA256,
                  'source_bytecode': 'plugin.pyo / Python 2.6',
                  'signature_reference': 'plugin.py312o / Python 3.12',
                  'identical_signature_inventory': True,
                  'objects': oldest,
                  'converted_source_sha256': hashlib.sha256(converted.encode()).hexdigest(),
                  'limits': 'Syntax and signature parity are not proof of behavioral equivalence.'}
        destination.with_suffix('.inventory.json').write_text(json.dumps(record, indent=2)+'\n')
        print('Recovered', len(oldest), 'code objects;', len(converted), 'source characters')


if __name__ == '__main__':
    def timed_out(*args):
        raise TimeoutError('Source recovery exceeded 180 seconds')
    signal.signal(signal.SIGALRM, timed_out)
    signal.alarm(180)
    recover(sys.argv[1], sys.argv[2])
