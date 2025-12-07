
# tests/test_rules_unittest.py
import unittest

from src.rules import study_mode

class StudyModeTests(unittest.TestCase):

    def test_focused_returns_deep_study(self):
        self.assertEqual(study_mode("focused"), "deep study")

    def test_tired_returns_light_review(self):
        self.assertEqual(study_mode("tired"), "light review")

    def test_unknown_state_uses_safe_default(self):
        self.assertEqual(study_mode("incredibly hyped!!!"), "basic check-in")

    def test_non_string_input_uses_safe_default(self):
        self.assertEqual(study_mode(123), "basic check-in")


if __name__ == "__main__":
    unittest.main()
