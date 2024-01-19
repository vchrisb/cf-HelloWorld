import unittest

from hello import app


class FlaskBasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        """Assert that user successfully lands on homepage"""
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_live_status_code(self):
        """Assert that liveness returns 200"""
        result = self.app.get("/healthz/live")
        self.assertEqual(result.status_code, 200)

    def test_ready_status_code(self):
        """Assert that readiness returns 200"""
        result = self.app.get("/healthz/ready")
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
