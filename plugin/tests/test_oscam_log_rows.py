import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('log_rows_contracts',ROOT/'warder_log_rows.py')
ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(ui)
def builder(pos=(0,0),size=(0,0),font=0,text='',color=None,color_sel=None,backcolor=None,backcolor_sel=None):
    return (0,*pos,*size,font,0,text,color,color_sel,backcolor,backcolor_sel)

class LogRowTests(unittest.TestCase):
    def test_extreme_line_and_whitespace_keep_all_content_and_original_identity(self):
        value='W'*3000+'   '+('dlhý text  '*100)
        result=ui.rows([[value,builder(text=value,color=0xff3300)]],builder,1347,24,32)
        self.assertEqual(''.join(item[1][7] for item in result),value)
        self.assertTrue(all(item[0]==value and item[1][4]==32 for item in result))
        self.assertTrue(all(item[1][8]==0xff3300 for item in result))
        self.assertTrue(all(len(item[1][7])<=1347//24 for item in result))
    def test_explicit_blank_lines_and_empty_message_keep_readable_rows(self):
        result=ui.rows([['id',builder(text='a\n\nb')]],builder,100,10,24)
        self.assertEqual([item[1][7] for item in result],['a','','b'])
    def test_selected_and_background_colors_are_retained(self):
        result=ui.rows([['id',builder(text='sample',color=1,color_sel=2,backcolor=3,backcolor_sel=4)]],builder,100,10,24)
        self.assertEqual(result[0][1][8:12],(1,2,3,4))

if __name__=='__main__':unittest.main()
