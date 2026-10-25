"""Mechanically size approved transparent hardware masters for Enigma2.

Uses ImageMagick on the build machine only; never installed on the receiver.
No matte, recoloring, background removal or generative edits are performed here.
"""
from pathlib import Path
import subprocess

BASE=Path(__file__).resolve().parents[1]
NAMES=('mem','swap','summ','root','hdd','usb','cf','sd','hdd_temp','cpu','sensor','lr','updown')


def prepare():
    for name in NAMES:
        source=BASE/'artwork/system-raster'/(name+'.png')
        output=BASE/'src/GlassSysUtil/images'/('system-'+name+'.png')
        subprocess.run(['convert',str(source),'-trim','+repage','-resize','100x100','-background','none','-gravity','center','-extent','120x120','-strip','PNG32:'+str(output)],check=True)

if __name__=='__main__':prepare()
