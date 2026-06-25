import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.routes.field import fields_db
from app.routes.detection import build_detection_report


class DetectionReportTest(unittest.TestCase):
    def setUp(self):
        fields_db.clear()
        fields_db.extend(
            [
                {
                    "id": 1,
                    "name": "A区",
                    "location": "东区",
                    "area": 10,
                    "crop_type": "番茄",
                    "soil_moisture": 22,
                    "temperature": 38,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00",
                },
                {
                    "id": 2,
                    "name": "B区",
                    "location": "西区",
                    "area": 8,
                    "crop_type": "玉米",
                    "soil_moisture": 72,
                    "temperature": 24,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00",
                },
            ]
        )

    def test_build_detection_report_flags_alerts(self):
        report = build_detection_report(fields_db)

        self.assertEqual(report["summary"]["total_fields"], 2)
        self.assertEqual(report["summary"]["warning_count"], 2)
        self.assertEqual(report["summary"]["critical_count"], 1)
        self.assertTrue(any(item["type"] == "critical" for item in report["alerts"]))
        self.assertTrue(any(item["title"] == "土壤湿度偏低" for item in report["alerts"]))


if __name__ == "__main__":
    unittest.main()
