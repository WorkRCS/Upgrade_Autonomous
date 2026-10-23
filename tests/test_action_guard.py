import unittest

from core.action_guard import confirmation_requirement


class ConfirmationRequirementTests(unittest.TestCase):
    def test_file_delete_asks_for_exact_target_confirmation(self):
        reason = confirmation_requirement(
            "file_controller",
            {"action": "delete", "path": "Documents", "name": "old-report.pdf"},
        )
        self.assertIsNotNone(reason)
        self.assertIn("old-report.pdf", reason)
        self.assertIn("Trash", reason)

    def test_permanent_delete_explains_irreversibility(self):
        reason = confirmation_requirement(
            "file_controller",
            {"action": "delete_permanent", "path": "Downloads", "name": "archive"},
        )
        self.assertIsNotNone(reason)
        self.assertIn("cannot be undone", reason)
        self.assertIn("Downloads/archive", reason)

    def test_model_supplied_confirmed_flag_does_not_bypass_policy(self):
        reason = confirmation_requirement(
            "computer_settings", {"action": "shutdown", "confirmed": "yes"}
        )
        self.assertIsNotNone(reason)
        self.assertIn("Shut down", reason)

    def test_app_termination_and_restart_require_confirmation(self):
        for action in ("close_app", "close_window", "restart"):
            with self.subTest(action=action):
                self.assertIsNotNone(confirmation_requirement("computer_settings", {"action": action}))

    def test_message_confirmation_does_not_expose_message_body(self):
        secret = "private sentence and password p@ssword"
        reason = confirmation_requirement(
            "send_message",
            {"platform": "WhatsApp", "receiver": "Alex", "message_text": secret},
        )
        self.assertIn("WhatsApp", reason)
        self.assertIn("Alex", reason)
        self.assertNotIn(secret, reason)

    def test_destructive_shell_commands_are_confirmed(self):
        commands = (
            "rm -rf /tmp/build",
            "docker rm -f test-container",
            "kubectl delete pod app-123",
            "db.dropDatabase()",
            "winget uninstall Docker Desktop",
            "git push --force origin main",
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertIsNotNone(
                    confirmation_requirement("computer_control", {"action": "type", "text": command})
                )

    def test_ordinary_shell_commands_are_not_blocked(self):
        for command in ("python app.py", "git status", "docker ps", "npm test"):
            with self.subTest(command=command):
                self.assertIsNone(
                    confirmation_requirement("computer_control", {"action": "type", "text": command})
                )

    def test_normal_browser_navigation_does_not_require_confirmation(self):
        self.assertIsNone(
            confirmation_requirement("browser_control", {"action": "go_to", "url": "https://example.com"})
        )


if __name__ == "__main__":
    unittest.main()
