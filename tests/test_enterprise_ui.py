"""Behavioral gates for the desktop workspace; no API or hardware requests."""
import json
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')


class WorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import ui
            from PyQt6.QtWidgets import QApplication
        except ImportError as exc:
            if os.environ.get('CI') == 'true':
                raise
            raise unittest.SkipTest(str(exc))
        cls.ui = ui
        cls.app = QApplication.instance() or QApplication([])
        cls.tmp = tempfile.TemporaryDirectory()
        cls.original = ui.API_FILE
        ui.API_FILE = Path(cls.tmp.name) / 'api_keys.json'
        ui.API_FILE.write_text(json.dumps({'gemini_api_key': 'test', 'os_system': 'Linux'}))

    @classmethod
    def tearDownClass(cls):
        cls.ui.API_FILE = cls.original
        cls.tmp.cleanup()

    def setUp(self):
        self.window = self.ui.MainWindow('')
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()

    def test_transcript_is_plain_and_diagnostics_stay_out(self):
        view = self.window._conversation
        view.append_line('NET: private diagnostic')
        self.assertNotIn('private diagnostic', view.toPlainText())
        view.append_line('You: <script>literal text</script>')
        self.assertIn('<script>literal text</script>', view.toPlainText())
        self.assertNotIn('How can I help', view.toPlainText())

    def test_remove_attachment_clears_all_selection_state(self):
        window = self.window
        window._drop_zone._set_file(str(self.ui.API_FILE))
        self.assertEqual(window._current_file, str(self.ui.API_FILE))
        window._drop_zone.clear_file()
        self.assertIsNone(window._current_file)
        self.assertIsNone(window._drop_zone.current_file())
        self.assertIn('No file selected', window._file_hint.text())

    def test_theme_dialog_scrolls_and_escape_restores_preview(self):
        from PyQt6.QtWidgets import QScrollArea
        window = self.window
        original = self.ui.current_palette()
        window._open_customize()
        dialog = window._customize_overlay
        self.app.processEvents()
        self.assertIsNotNone(dialog.findChild(QScrollArea))
        dialog._set_color('#45a37d')
        self.assertNotEqual(original, self.ui.current_palette())
        dialog.reject()
        self.assertEqual({k:v.lower() for k,v in original.items()}, self.ui.current_palette())
        self.assertFalse(dialog.isVisible())

    def test_confirmation_timeout_rejects_and_releases_waiter(self):
        import threading
        state = {'event': threading.Event(), 'confirmed': False, 'timeout': .02}
        self.window._show_action_confirmation('Test', 'No action will run.', state)
        self.assertTrue(state['event'].is_set())
        self.assertFalse(state['confirmed'])

    def test_reduced_motion_keeps_real_input_meter(self):
        hud = self.window.hud
        hud.reduced_motion = True
        hud.state = 'LISTENING'
        tick = hud._tick
        hud.set_input_level(.8, 'PC')
        hud._step()
        self.assertEqual(hud._tick, tick)
        self.assertGreater(hud._mic_level, .5)

    def test_compact_window_keeps_composer_and_context_visible(self):
        window = self.window
        window.resize(840, 560)
        self.app.processEvents()
        for widget in [window._input, window._mute_btn, window._context_tabs]:
            self.assertTrue(widget.isVisible())
            point = widget.mapTo(window, widget.rect().bottomRight())
            self.assertLessEqual(point.x(), window.width())
            self.assertLessEqual(point.y(), window.height())

    def test_preferences_save_error_keeps_form_and_draft(self):
        from unittest.mock import patch
        self.window._open_customize()
        dialog = self.window._customize_overlay
        dialog._user_input.setText('Retain my draft')
        with patch.object(Path, 'replace', side_effect=PermissionError('test')):
            dialog._save()
        self.assertTrue(dialog.isVisible())
        self.assertEqual(dialog._user_input.text(), 'Retain my draft')
        self.assertIn('Could not save', dialog._feedback.text())
        dialog.reject()

    def test_camera_workspace_returns_to_voice_rail(self):
        window = self.window
        window._on_cam_stream(True)
        self.app.processEvents()
        self.assertEqual(window._center_split.widget(0), window._hud_cam_stack)
        window._on_cam_stream(False)
        self.app.processEvents()
        self.assertEqual(window._center_split.widget(0), window._conversation)
        self.assertEqual(window._hud_cam_stack.currentIndex(), 0)
