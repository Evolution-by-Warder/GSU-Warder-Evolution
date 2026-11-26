import importlib.util
import json
from pathlib import Path
import re
import tempfile
import types
import unittest
from unittest.mock import patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('gsu_i18n',ROOT/'i18n.py')
i18n=importlib.util.module_from_spec(spec);spec.loader.exec_module(i18n)


class LocalizationTests(unittest.TestCase):
    def test_all_twenty_one_catalogs_have_common_keys_and_safe_format_arguments(self):
        english=json.loads((ROOT/'locale/en.json').read_text())
        self.assertGreaterEqual(len(english),141)
        self.assertEqual(len(i18n.LANGUAGES),21)
        for lang in i18n.LANGUAGES:
            values=json.loads((ROOT/'locale'/(lang+'.json')).read_text())
            self.assertFalse(set(english)-set(values),lang)
            for key,value in values.items():
                self.assertIsInstance(value,str)
                self.assertTrue(value)
                self.assertEqual(re.findall(r'%[sdi]',key),re.findall(r'%[sdi]',value),(lang,key))
            if lang!='en':self.assertNotEqual(i18n.translate('System Information',lang),'System Information')

    def test_legacy_destructive_operation_warnings_are_translated(self):
        extra=json.loads((ROOT/'locale/legacy-supplement.json').read_text(encoding='utf-8'))
        self.assertEqual(set(extra),set(i18n.LANGUAGES))
        self.assertEqual(len(extra['en']),137)
        for code,catalog in extra.items():
            self.assertEqual(set(catalog),set(extra['en']))
            for key,value in catalog.items():
                self.assertTrue(value)
                if code!='en' and value!=key:
                    self.assertNotEqual(i18n.translate(key,code),key,(code,key))
                elif code!='en':
                    self.assertIn(key,('Disk','Source','Destination','Partition'),(code,key))

    def test_normalizes_regions_and_falls_back_to_english_without_global_locale(self):
        for code in ('sk_SK','SK-sk','sk'):
            self.assertEqual(i18n.translate('Settings',code),'Nastavenia')
        for code in ('xx_XX','../../sk',None,'en_GB'):
            self.assertEqual(i18n.translate('Settings',code),'Settings')
        self.assertEqual(i18n.translate('A missing sentence','ru'),'A missing sentence')
        for alias,expected in (('sq_AL','al'),('gr-GR','el'),('cz_CZ','cs'),('ua_UA','uk'),('cn_CN','zh')):
            self.assertEqual(i18n.language(alias),expected)
            self.assertEqual(i18n.translate('Settings',alias),i18n.translate('Settings',expected))
        with patch('locale.setlocale',side_effect=AssertionError('global locale changed')):
            self.assertEqual(i18n.translate('Back','fr'),'Retour')

    def test_catalog_is_loaded_once_and_missing_or_corrupt_catalog_is_safe(self):
        i18n.catalog.cache_clear()
        with patch.object(Path,'read_text',wraps=None) as read:
            read.return_value='{"Back":"Retour"}'
            for _ in range(10):self.assertEqual(i18n.translate('Back','fr',root='/nonexistent-test'),'Retour')
            self.assertEqual(read.call_count,1)
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder)/'locale';base.mkdir();(base/'de.json').write_text('broken')
            self.assertEqual(i18n.translate('Back','de',root=folder),'Back')

    def test_original_slovak_gettext_catalog_remains_a_fallback(self):
        import gettext,tarfile
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder)/'locale/sk/LC_MESSAGES';base.mkdir(parents=True)
            with tarfile.open(ROOT.parents[1]/'resources.tar.gz') as archive:
                raw=archive.extractfile('locale/sk/LC_MESSAGES/gsu.mo').read()
            (base/'gsu.mo').write_bytes(raw)
            with (base/'gsu.mo').open('rb') as stream:old=gettext.GNUTranslations(stream)
            key=next(k for k,v in old._catalog.items() if isinstance(k,str) and k and isinstance(v,str) and v and k!=v)
            self.assertEqual(i18n.translate(key,'sk',root=folder),old.gettext(key))

    def test_plugin_tracks_system_language_and_respects_localization_switch(self):
        plugin=load(ROOT)
        with patch.object(plugin,'GSU_PATH',str(ROOT)+'/'), patch.object(plugin.config.osd.language,'value','sk_SK'), patch.object(plugin.config.plugins.GlassSysUtil.par62,'value',True):
            for lang in i18n.LANGUAGES:
                plugin.config.osd.language.value=lang+'_XX'
                self.assertEqual(plugin._('Settings'),i18n.translate('Settings',lang))
            plugin.config.plugins.GlassSysUtil.par62.value=False
            self.assertEqual(plugin._('Settings'),'Settings')
            self.assertEqual(plugin._warder_main.text(vars(plugin),'Settings'),'Settings')
            plugin.config.plugins.GlassSysUtil.par62.value=True

    def test_calendar_covers_every_supported_language(self):
        from datetime import datetime
        plugin=load(ROOT)
        main=plugin._warder_main
        self.assertEqual(set(main.DAYS),set(i18n.LANGUAGES))
        self.assertEqual(set(main.MONTHS),set(i18n.LANGUAGES))
        for lang in i18n.LANGUAGES:
            self.assertEqual(len(main.DAYS[lang]),7,lang)
            self.assertEqual(len(main.MONTHS[lang]),12,lang)
            day,date,clock,seconds=main.clock_values(datetime(2026,11,26,12,34,56),lang)
            self.assertEqual(day,main.DAYS[lang][3])
            self.assertIn('2026',date)
            self.assertEqual((clock,seconds),('12:34',':56'))
        self.assertEqual(main.clock_values(datetime(2026,11,26),'cn_CN')[1],'2026年11月26日')

    def test_translated_system_labels_keep_layout_and_data_separate(self):
        from xml.etree import ElementTree as ET
        plugin=load(ROOT)
        translate=lambda key:i18n.translate(key,'de')
        root=ET.fromstring(plugin._warder_system.system_skin(plugin.GlassSysInfo,1920,1080,translator=translate))
        self.assertTrue(any(n.get('text')=='Prozesse' for n in root))
        self.assertTrue(any(n.get('text')=='Protokolle:' for n in root))
        self.assertIsNotNone(root.find("widget[@name='ProccessInfo']"))

    def test_builder_includes_catalogs_without_external_gettext_dependency(self):
        import sys,io,tarfile
        sys.path.insert(0,str(ROOT.parents[1]/'tools'))
        import build_ipk
        with tempfile.TemporaryDirectory() as folder:
            raw=build_ipk.build(folder).read_bytes()
            offset=8;data=None;control=None
            while offset<len(raw):
                header=raw[offset:offset+60];size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
                value=raw[offset+60:offset+60+size];offset+=60+size+size%2
                if name=='data.tar.gz':data=value
                if name=='control.tar.gz':control=value
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                names={m.name.removeprefix('./') for m in archive}
                prefix=build_ipk.PLUGIN+'/locale/'
                for lang in i18n.LANGUAGES:self.assertIn(prefix+lang+'.json',names)
                self.assertIn(prefix+'legacy-supplement.json',names)
                self.assertIn(prefix+'sk/LC_MESSAGES/gsu.mo',names)
            with tarfile.open(fileobj=io.BytesIO(control)) as archive:
                self.assertNotIn(b'python3-gettext',archive.extractfile('./control').read())
