"""Static checks for worker-page calls that require a Supabase access token."""

import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKER_PAGE = REPOSITORY_ROOT / "frontend" / "worker_jobs.html"


class WorkerPageAuthenticationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKER_PAGE.read_text(encoding="utf-8")

    def assert_authenticated_request(self, pattern):
        self.assertRegex(self.source, pattern)

    def test_application_submission_uses_authenticated_api_helper(self):
        self.assert_authenticated_request(
            r"window\.lnmRequest\('/applications/apply',\s*\{"
            r"\s*method:\s*'POST',\s*authenticated:\s*true"
        )

    def test_worker_recommendations_use_authenticated_api_helper(self):
        self.assert_authenticated_request(
            r"window\.lnmRequest\(`/recommend/jobs/\$\{encodeURIComponent\(workerId\)\}`,"
            r"\s*\{\s*authenticated:\s*true\s*\}\)"
        )

    def test_application_history_uses_authenticated_api_helper(self):
        self.assert_authenticated_request(
            r"window\.lnmRequest\(`/applications/my-applications/"
            r"\$\{encodeURIComponent\(workerId\)\}`,\s*\{\s*authenticated:\s*true\s*\}\)"
        )


if __name__ == "__main__":
    unittest.main()
