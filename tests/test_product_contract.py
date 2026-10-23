from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProductContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ui = (ROOT / "ui.py").read_text(encoding="utf-8")
        cls.main = (ROOT / "main.py").read_text(encoding="utf-8")
        cls.prompt = (ROOT / "core" / "prompt.txt").read_text(encoding="utf-8")
        cls.app = (ROOT / "dashboard" / "static" / "app.html").read_text(encoding="utf-8")
        cls.login = (ROOT / "dashboard" / "static" / "login.html").read_text(encoding="utf-8")
        cls.readme = (ROOT / "readme.md").read_text(encoding="utf-8")

    def test_desktop_is_brand_neutral(self):
        self.assertIn('UI_BRAND = "AI ASSISTANT"', self.ui)
        self.assertIn('self.setWindowTitle("AI ASSISTANT • DESKTOP")', self.ui)
        self.assertIn('self._sub_lbl.setText("VOICE  •  VISION  •  AUTOMATION")', self.ui)
        self.assertNotIn("self._name_input", self.ui)
        self.assertNotIn("MARK LI", self.ui)
        self.assertNotIn("EDITH SYSTEMS", self.ui)
        self.assertNotIn("EVEN DEAD, I'M THE HERO", self.ui)

    def test_hud_uses_a_neutral_generated_visual(self):
        self.assertIn("self._face_px = None", self.ui)
        self.assertIn("def _build_assistant_icon(", self.ui)
        self.assertIn('config" / "assistant.ico"', self.ui)
        self.assertNotIn("config" / "jarvis.ico", self.ui)

    def test_gemini_model_is_preserved_and_voice_is_configured(self):
        self.assertIn('LIVE_MODEL          = "models/gemini-2.5-flash-native-audio-preview-12-2025"', self.main)
        self.assertIn('voice_name="Kore"', self.main)
        self.assertIn("configured feminine voice", self.main.lower())
        self.assertIn("confident, mature, warm, clear, and decisive", self.main)

    def test_assistant_instructions_are_unbranded_and_action_focused(self):
        for name in ("JARVIS", "EDITH", "Ultron", "Iron Man", "Tony Stark"):
            self.assertNotIn(name.lower(), self.prompt.lower())
        self.assertIn("start the relevant action immediately", self.prompt)
        self.assertIn("Never claim an action succeeded until the tool confirms success", self.prompt)

    def test_remote_pages_use_neutral_visible_names(self):
        self.assertIn("<title>AI Assistant • Remote</title>", self.app)
        self.assertIn('<div class="logo">AI <em>ASSISTANT</em></div>', self.app)
        self.assertIn("<title>AI Assistant • Remote Access</title>", self.login)
        self.assertIn('<div class="logo">AI <em>ASSISTANT</em></div>', self.login)
        for content in (self.app, self.login):
            self.assertNotIn("EDITH", content)
            self.assertNotIn("MARK LI", content)

    def test_existing_remote_protocol_contract_is_retained(self):
        # These internal identifiers are compatibility keys, not visible product branding.
        self.assertIn("jarvis_token", self.app)
        self.assertIn("jarvis_key", self.app)
        self.assertIn("JARVIS-DASHBOARD-v1", self.app)
        self.assertIn("jarvis_device_token", self.login)
        self.assertIn("speaker === 'jarvis'", self.app)

    def test_documentation_does_not_advertise_character_branding(self):
        for name in ("JARVIS", "EDITH", "Ultron", "Tony Stark", "Iron Man"):
            self.assertNotIn(name.lower(), self.readme.lower())
        self.assertIn("Upgrade_Autonomous.git", self.readme)


if __name__ == "__main__":
    unittest.main()
