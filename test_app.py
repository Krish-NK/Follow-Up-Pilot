import tempfile
import unittest
from pathlib import Path

import app as followup_app


class FollowUpPilotTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db = followup_app.DB_PATH
        followup_app.DB_PATH = Path(self.temp_dir.name) / "test.db"
        followup_app.init_db()
        followup_app.app.config.update(TESTING=True)
        self.client = followup_app.app.test_client()

    def tearDown(self):
        followup_app.DB_PATH = self.original_db
        self.temp_dir.cleanup()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"FollowUpPilot", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_create_and_list_lead(self):
        response = self.client.post("/api/leads", json={
            "name": "Test Customer",
            "company": "Example Co",
            "status": "Interested",
            "value": 15000
        })
        self.assertEqual(response.status_code, 201)
        listing = self.client.get("/api/leads")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.get_json()[0]["name"], "Test Customer")

    def test_reject_negative_deal_value(self):
        response = self.client.post("/api/leads", json={
            "name": "Invalid Customer",
            "status": "New",
            "value": -100
        })
        self.assertEqual(response.status_code, 400)

    def test_missing_lead_returns_json_404(self):
        response = self.client.get("/api/leads/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
