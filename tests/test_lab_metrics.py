import unittest
from automation.lab_automation_core import LabMetrics
from datetime import datetime

class TestLabMetrics(unittest.TestCase):
    def test_lab_metrics_creation(self):
        now = datetime.now()
        metrics = LabMetrics(
            timestamp=now,
            staff_member="John Doe",
            shift="Day",
            samples_processed=100,
            error_count=2,
            break_time_minutes=30,
            qc_completion_percent=98.5,
            tat_target_met=True,
            performance_score=85.0,
            supervisor="Jane Smith"
        )
        self.assertEqual(metrics.staff_member, "John Doe")
        self.assertTrue(metrics.tat_target_met)
        self.assertGreaterEqual(metrics.qc_completion_percent, 95)

if __name__ == "__main__":
    unittest.main()
