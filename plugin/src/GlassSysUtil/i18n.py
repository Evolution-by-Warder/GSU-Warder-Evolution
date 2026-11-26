"""Plugin-local translations, cached by language; never change Enigma2's locale."""
from functools import lru_cache
import gettext
import json
from pathlib import Path

LANGUAGES=('en','sk','cs','de','pl','hu','ru','fr','it','es','al','el','et','fa','lt','nl','pt','ro','tr','uk','zh')
ALIASES={'sq':'al','gr':'el','cz':'cs','ua':'uk','cn':'zh'}
ROOT=Path(__file__).parent


def language(value):
    code=str(value or 'en').replace('-','_').split('_')[0].lower()
    code=ALIASES.get(code,code)
    return code if code in LANGUAGES else 'en'


@lru_cache(maxsize=32)
def catalog(root,code):
    base=Path(root)/'locale'
    try:
        values=json.loads((base/(code+'.json')).read_text(encoding='utf-8'))
        if not isinstance(values,dict):values={}
    except (OSError,ValueError):values={}
    try:original=gettext.translation('gsu',str(base),languages=[code],fallback=True)
    except (OSError,ValueError,EOFError):original=gettext.NullTranslations()
    supplement={}
    path=base/'legacy-supplement.json'
    if path.is_file():
        try:
            all_values=json.loads(path.read_text(encoding='utf-8'))
            candidate=all_values.get(code,{}) if isinstance(all_values,dict) else {}
            if isinstance(candidate,dict):supplement=candidate
        except (OSError,ValueError):pass
    return values,original,supplement


def translate(value,locale='en',root=None):
    code=language(locale)
    if code=='en':return value
    values,original,supplement=catalog(str(ROOT if root is None else root),code)
    result=values.get(value)
    if isinstance(result,str) and result:return result
    legacy=original.gettext(value)
    if legacy!=value:return legacy
    result=supplement.get(value)
    return result if isinstance(result,str) and result else value


def for_api(api,value,fallback=None):
    settings=api.get('config')
    enabled=getattr(getattr(getattr(getattr(settings,'plugins',None),'GlassSysUtil',None),'par62',None),'value',True)
    if not enabled:return value
    locale=getattr(getattr(getattr(settings,'osd',None),'language',None),'value','en')
    translated=api.get('_',lambda key:key)(value)
    if translated!=value:return translated
    translated=translate(value,locale)
    if translated==value and language(locale)=='sk' and fallback:return fallback.get(value,value)
    return translated
