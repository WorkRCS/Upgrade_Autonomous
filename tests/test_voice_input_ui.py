"""Regression coverage for EDITH's real-input, display-only HUD feedback."""
import struct
import unittest
from pathlib import Path

from core.audio_meter import pcm16_level

ROOT = Path(__file__).resolve().parents[1]


class PcmMeterTests(unittest.TestCase):
    def test_silence_is_zero(self):
        self.assertEqual(pcm16_level(b"\x00\x00" * 1024), 0.0)
        self.assertEqual(pcm16_level(b""), 0.0)

    def test_louder_pcm_creates_stronger_signal(self):
        quiet = struct.pack("<h", 100) * 1024
        speech = struct.pack("<h", 5000) * 1024
        self.assertGreater(pcm16_level(speech), pcm16_level(quiet))
        self.assertGreater(pcm16_level(speech), 0.11)

    def test_clamped_and_odd_length_are_safe(self):
        loud = struct.pack("<h", 32767) * 200
        self.assertLessEqual(pcm16_level(loud), 1.0)
        self.assertGreater(pcm16_level(loud), 0.0)
        self.assertEqual(pcm16_level(b"\x7f"), 0.0)
        self.assertEqual(pcm16_level(None), 0.0)

    def test_buffer_views_are_supported(self):
        raw = struct.pack("<h", 3000) * 600
        self.assertEqual(pcm16_level(raw), pcm16_level(memoryview(raw)))


class VoiceHudWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ui = (ROOT / "ui.py").read_text(encoding="utf-8")
        cls.main = (ROOT / "main.py").read_text(encoding="utf-8")

    def test_input_is_real_pcm_not_random_animation(self):
        self.assertIn("from core.audio_meter          import pcm16_level", self.main)
        self.assertIn("pcm16_level(data)", self.main)
        self.assertIn("loop.call_soon_threadsafe(", self.main)
        self.assertIn('self._publish_mic_activity, data, "PC"', self.main)
        self.assertIn('self._publish_mic_activity(data, "PHONE")', self.main)
        self.assertIn("_mic_level_sig  = pyqtSignal(float, str)", self.ui)
        self.assertIn('def show_input_level(self, level: float, source: str = "PC")', self.ui)
        self.assertIn("self._mic_level_sig.connect(self._on_mic_level)", self.ui)

    def test_state_clear_and_real_mic_timeout(self):
        self.assertIn("def clear_input_level(self) -> None:", self.ui)
        self.assertIn("self.hud.clear_input_level()", self.ui)
        self.assertIn("(now - self._mic_last_packet) < 0.65", self.ui)
        self.assertIn("self._mic_level > 0.08", self.ui)
        self.assertIn("WAITING FOR MIC AUDIO", self.ui)
        self.assertIn("AUDIO DETECTED", self.ui)

    def test_existing_stream_and_cloud_provider_unchanged(self):
        self.assertIn("await self.session.send_realtime_input(media=msg)", self.main)
        self.assertIn('LIVE_MODEL          = "models/gemini-2.5-flash-native-audio-preview-12-2025"', self.main)
        self.assertIn("enqueue_latest_audio(self.out_queue, chunk)", self.main)
        self.assertIn("self._tmr.start(33)", self.ui)
        self.assertIn("self.hud.speaking = (state == \"SPEAKING\")", self.ui)


if __name__ == "__main__":
    unittest.main()
