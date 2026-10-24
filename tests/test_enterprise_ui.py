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

    def test_camera_workspace_returns_to_center_animation(self):
        window = self.window
        window._on_cam_stream(True)
        self.app.processEvents()
        self.assertEqual(window._center_split.widget(0), window._hud_cam_stack)
        window._on_cam_stream(False)
        self.app.processEvents()
        self.assertEqual(window._center_split.widget(0), window._hud_cam_stack)
        self.assertEqual(window._center_split.widget(1), window._conversation)
        self.assertEqual(window._hud_cam_stack.currentIndex(), 0)

    def test_window_controls_minimize_maximize_restore_and_close(self):
        from PyQt6.QtCore import Qt
        from PyQt6.QtTest import QTest
        window = self.window
        buttons = window._window_controls
        for hint in [Qt.WindowType.WindowCloseButtonHint, Qt.WindowType.WindowMinimizeButtonHint,
                     Qt.WindowType.WindowMaximizeButtonHint]:
            self.assertTrue(window.windowFlags() & hint)
        QTest.mouseClick(buttons.minimize_button, Qt.MouseButton.LeftButton)
        self.app.processEvents()
        self.assertTrue(window.isMinimized())
        window.showNormal()
        self.app.processEvents()
        QTest.mouseClick(buttons.maximize_button, Qt.MouseButton.LeftButton)
        self.app.processEvents()
        self.assertTrue(window.isMaximized())
        self.assertEqual(buttons.maximize_button.accessibleName(), 'Restore window')
        QTest.mouseClick(buttons.maximize_button, Qt.MouseButton.LeftButton)
        self.app.processEvents()
        self.assertFalse(window.isMaximized())
        self.assertEqual(buttons.maximize_button.accessibleName(), 'Maximize window')
        QTest.mouseClick(buttons.close_button, Qt.MouseButton.LeftButton)
        self.app.processEvents()
        self.assertFalse(window.isVisible())

    def test_fullscreen_still_has_accessible_window_controls(self):
        window = self.window
        window._toggle_fullscreen()
        self.app.processEvents()
        self.assertTrue(window.isFullScreen())
        self.assertTrue(window._window_controls.close_button.isVisible())
        self.assertTrue(window._window_controls.minimize_button.isVisible())
        window._window_controls.maximize_button.click()
        self.app.processEvents()
        self.assertFalse(window.isFullScreen())

    def test_in_app_dialog_close_reverts_theme(self):
        from PyQt6.QtWidgets import QPushButton
        window = self.window
        original = self.ui.current_palette()
        window._open_customize()
        dialog = window._customize_overlay
        self.app.processEvents()
        dialog._set_color('#a0458c')
        close = next(b for b in dialog.findChildren(QPushButton)
                     if b.accessibleName() == 'Close dialog')
        close.click()
        self.app.processEvents()
        self.assertFalse(dialog.isVisible())
        self.assertEqual({k: v.lower() for k, v in original.items()}, self.ui.current_palette())

    def test_compact_content_result_can_be_read_and_dismissed(self):
        window = self.window
        window.resize(840, 560)
        window._show_content('Analysis', 'A verified tool result')
        self.app.processEvents()
        self.assertTrue(window._content_panel.isVisible())
        self.assertFalse(window._conversation.isVisible())
        self.assertGreater(window._content_display.height(), 40)
        window._dismiss_content()
        self.app.processEvents()
        self.assertTrue(window._conversation.isVisible())
        self.assertFalse(window._content_panel.isVisible())

    def test_initial_geometry_preserves_title_bar_and_screen_origin(self):
        from PyQt6.QtCore import QRect
        from core.window_controls import initial_geometry
        for screen in [QRect(0, 0, 1366, 720), QRect(-1920, 40, 1920, 1040),
                       QRect(1920, 30, 1280, 690)]:
            geometry = initial_geometry(screen, 1180, 780)
            self.assertTrue(screen.contains(geometry))
            self.assertGreaterEqual(geometry.top(), screen.top()+32)
            self.assertLessEqual(geometry.bottom(), screen.bottom()-16)
