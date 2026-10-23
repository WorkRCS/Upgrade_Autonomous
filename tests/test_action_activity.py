import unittest

from core.action_activity import activity_outcome, describe_tool_activity


class ActionActivityTests(unittest.TestCase):
    def test_generic_desktop_app_is_visible_in_activity(self):
        label = describe_tool_activity("open_app", {"app_name": "Docker Desktop"})
        self.assertIn("Docker Desktop", label)
        self.assertIn("desktop app", label.lower())

    def test_typing_content_is_not_logged(self):
        secret = "this is private user text"
        label = describe_tool_activity("computer_control", {"action": "type", "text": secret})
        self.assertNotIn(secret, label)
        self.assertIn("content hidden", label)

    def test_message_body_is_not_logged(self):
        secret = "please send my password 123"
        label = describe_tool_activity(
            "send_message",
            {"platform": "WhatsApp", "receiver": "Alex", "message_text": secret},
        )
        self.assertNotIn(secret, label)
        self.assertIn("WhatsApp", label)
        self.assertIn("Alex", label)

    def test_browser_url_does_not_include_query_or_fragment(self):
        label = describe_tool_activity(
            "browser_control",
            {"action": "go_to", "url": "https://example.com/path?token=private#section"},
        )
        self.assertIn("https://example.com/path", label)
        self.assertNotIn("private", label)
        self.assertNotIn("section", label)

    def test_results_are_classified_without_echoing_contents(self):
        self.assertEqual(activity_outcome("Opened WhatsApp."), "ok")
        self.assertEqual(activity_outcome("Could not launch app."), "error")
        self.assertEqual(activity_outcome("No results were found."), "warning")
        self.assertEqual(
            activity_outcome("Launch request submitted for Docker Desktop, but I could not verify that it opened."),
            "warning",
        )


if __name__ == "__main__":
    unittest.main()
