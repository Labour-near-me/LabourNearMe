
import unittest

from ml.engines.skill_taxonomy import (
    matched_required_skills,
    skills_match,
)


class SkillTaxonomyTests(unittest.TestCase):
    def test_case_and_whitespace_are_normalized(self):
        self.assertTrue(skills_match("  PLUMBER  ", "plumber"))

    def test_explicit_aliases_match(self):
        self.assertTrue(skills_match("plumbing work", "plumber"))
        self.assertTrue(
            skills_match("wiring installation", "electrical wiring")
        )

    def test_unrelated_trades_do_not_match(self):
        self.assertFalse(skills_match("plumber", "electrician"))
        self.assertFalse(skills_match("electrician", "plumber"))
        self.assertEqual(
            matched_required_skills({"plumber"}, {"electrician"}),
            set(),
        )

    def test_explicit_parent_trade_compatibility(self):
        self.assertTrue(
            skills_match("electrician", "electrical wiring")
        )
        self.assertTrue(
            skills_match("electrical wiring", "electrician")
        )

    def test_distinct_specific_skills_are_not_interchangeable(self):
        self.assertFalse(
            skills_match("electrical wiring", "switch repair")
        )

    def test_matched_requirements_are_canonical_names(self):
        self.assertEqual(
            matched_required_skills(
                {"plumbing work"},
                {"plumber", "electrician"},
            ),
            {"plumber"},
        )


if __name__ == "__main__":
    unittest.main()
