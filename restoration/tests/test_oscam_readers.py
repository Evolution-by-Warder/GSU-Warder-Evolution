import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gsu_readers',ROOT/'src/GlassSysUtil/oscam_readers_parser.py')
readers=importlib.util.module_from_spec(spec);spec.loader.exec_module(readers)


def fixture(label='server',protocol='cs378x',enabled=True):
    action='disable' if enabled else 'enable'
    return ['<TR><TD CLASS="readercol0"><a data-next-action="%s" data-reader-name="%s"></a></TD>' % (action,label),
        '<TD CLASS="readercol1" data-sort-value="%s"><a>%s</a></TD>' % (label,label),
        '<TD CLASS="readercol2"><img TITLE="Protocol: %s"><span>online</span><span>192.168.10.6</span></TD>' % protocol,
        '<TD CLASS="readercol3"><div CLASS="groups">1,2</div></TD>',
        '<TD CLASS="readercol6">0 / 0</TD>',
        '<TD CLASS="readercol7">0 / 1 / 2 / 3</TD>',
        '<TD CLASS="readercol8">4 / 5 / 6 / 7</TD>',
        '<TD CLASS="readercol9">8 / 9 / 10 / 11</TD>',
        '<TD CLASS="readercol10">12 / 13 / 14 / 15</TD></TR>']


class ReaderTests(unittest.TestCase):
    def test_protocol_icon_status_address_and_counters_remain_separate(self):
        row=readers.parse_readers(fixture())[0]
        self.assertEqual(row['protocol'],'cs378x')
        self.assertEqual(row['status'],'online 192.168.10.6')
        self.assertEqual(row['counts'],['0 / 1 / 2 / 3','4 / 5 / 6 / 7','8 / 9 / 10 / 11','12 / 13 / 14 / 15'])
        self.assertTrue(row['enabled'])

    def test_reflowed_html_disabled_rows_and_entities(self):
        html=''.join(fixture('TV &amp; radio','newcamd',False)).lower()
        row=readers.parse_readers([html])[0]
        self.assertEqual(row['label'],'tv & radio')
        self.assertEqual(row['protocol'],'newcamd')
        self.assertFalse(row['enabled'])
        self.assertEqual(readers.parse_readers(['<html>Legacy content</html>']),[])
