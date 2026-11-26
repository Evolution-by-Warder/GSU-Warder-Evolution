"""Measure translated TV labels in reference fonts. Receiver skins can supply other fonts."""
from functools import lru_cache
from pathlib import Path
import sys
from xml.etree import ElementTree
from PIL import ImageFont

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'plugin/tests'),str(ROOT/'plugin/src')]
from receiver_stubs import load
load(ROOT/'plugin/src/GlassSysUtil')
from Plugins.Extensions.GlassSysUtil import i18n,warder_dashboard as view
from Plugins.Extensions.GlassSysUtil.warder_centres import CENTRES,DIAGNOSTICS

@lru_cache(maxsize=32)
def font(language,size):
    cjk=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
    return ImageFont.truetype(str(cjk) if language=='zh' and cjk.is_file() else 'DejaVuSans.ttf',size)


def measure():
    count=0
    for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
        screen=ElementTree.fromstring(view.skin(w,h,'overview'))
        footer=screen.find("widget[@name='blue']")
        footer_width=int(footer.get('size').split(',')[0])
        footer_size=int(footer.get('font').split(';')[1])
        for language in i18n.LANGUAGES:
            tr=lambda value:i18n.translate(value,language)
            labels=[tr(s) for _,s,_ in CENTRES]+[tr(s) for s,_ in DIAGNOSTICS.values()]
            foot=[tr(s) for s in ('Back','Pause','Start','Open plugin','Refresh','Export CSV','Select','Save','Live monitoring','Tuner interfaces')]
            foot.extend((tr('Interval')+' · 5 s',tr('Warning')+' · '+tr('yes')))
            for strings,limit,size in ((labels,round(960*w/1920),round(34*h/1080)),(foot,footer_width-8,footer_size)):
                for label in strings:
                    actual=font(language,size).getlength(label)
                    assert actual<=limit,(language,w,label,actual,limit)
                    count+=1
    print(count,'translated menu and key labels measured across 21 languages and four layouts')


if __name__=='__main__':
    measure()
