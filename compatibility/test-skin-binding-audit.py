"""Catch actual type/inheritance/skin-selection failures without receiver imports."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('binding_audit', Path(__file__).with_name('audit-openatv-skin-bindings.py'))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def check(self, controller, widget, extra_screens='', classes=''):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            modules = {
                'Components/GUIComponent.py': 'class GUIComponent: pass',
                'Components/Element.py': 'class Element: pass',
                'Components/Button.py': 'from Components.GUIComponent import GUIComponent\nclass Button(GUIComponent): pass',
                'Components/Sources/StaticText.py': 'from Components.Element import Element\nclass StaticText(Element): pass',
                'Components/TunerInfo.py': 'from Components.GUIComponent import GUIComponent\nclass TunerInfo(GUIComponent): pass',
                'Screens/Test.py': 'from Components.Button import Button as Caption\nfrom Components.Sources.StaticText import StaticText\nfrom Components.TunerInfo import TunerInfo\n' + classes + '\n' + controller,
            }
            for path, text in modules.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text + '\n')
            skin = root / 'skin.xml'
            skin.write_text('<skin><screen name="Dialog">%s</screen>%s</skin>' % (widget, extra_screens))
            return audit.audit(root, skin)

    def test_imported_alias_button_is_a_widget_not_a_source(self):
        result = self.check('class Dialog:\n def __init__(self): self["key_red"] = Caption()', '<widget source="key_red" render="Label"/>')
        self.assertEqual(len(result['binding_errors']), 1)
        self.assertEqual(result['binding_errors'][0]['constructor'], 'Components.Button.Button')

    def test_sources_must_use_source_renderer_binding(self):
        result = self.check('class Dialog:\n def __init__(self): self["text"] = StaticText()', '<widget name="text" render="Label"/>')
        self.assertEqual(result['binding_errors'][0]['expected_binding'], 'source')

    def test_inherited_fields_are_checked(self):
        result = self.check('class Dialog(Base): pass', '<widget source="key_red" render="Label"/>', classes='class Base:\n def __init__(self): self["key_red"] = Caption()')
        self.assertEqual(len(result['binding_errors']), 1)

    def test_qualified_import_distinguishes_tuner_widget_from_source(self):
        result = self.check('class Dialog:\n def __init__(self): self["snr"] = TunerInfo()', '<widget name="snr"/>')
        self.assertEqual(result['typed_widget_bindings_checked'], 1)
        self.assertFalse(result['binding_errors'])

    def test_explicit_skin_alias_bypasses_inactive_class_template(self):
        result = self.check('class Dialog:\n def __init__(self):\n  self["text"] = StaticText()\n  self.skinName = ["Missing", "Modern"]', '<widget name="text"/>', '<screen name="Modern"><widget source="text" render="Label"/></screen>')
        self.assertEqual(result['typed_widget_bindings_checked'], 1)
        self.assertFalse(result['binding_errors'])

    def test_inherited_ordered_fallback_does_not_check_unused_legacy_template(self):
        result = self.check('class Dialog(Base): pass', '<widget name="text"/>', '<screen name="Modern"><widget source="text" render="Label"/></screen>', 'class Base:\n def __init__(self):\n  self["text"] = StaticText()\n  self.skinName = [dynamic_name, "Modern", "Dialog"]')
        self.assertEqual(result['typed_widget_bindings_checked'], 2)  # Base and subclass both select Modern.
        self.assertFalse(result['binding_errors'])

    def test_conditional_and_excluded_widgets_follow_native_presence_rules(self):
        result = self.check('class Dialog:\n def __init__(self): self["text"] = StaticText()', '<widget name="text" conditional="missing"/><widget name="text" excludes="text"/><widget source="text" includes="text" render="Label"/>')
        self.assertEqual(result['typed_widget_bindings_checked'], 1)
        self.assertFalse(result['binding_errors'])

    def test_unknown_dynamic_constructor_is_reported_as_unresolved(self):
        result = self.check('class Dialog:\n def __init__(self): self["text"] = factory()', '<widget source="text" render="Label"/>')
        self.assertEqual(result['typed_widget_bindings_checked'], 0)
        self.assertEqual(result['unresolved_or_dynamic_widget_bindings'], 1)


if __name__ == '__main__':
    unittest.main()
