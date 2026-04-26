import unittest

from study_planner import infer_study_plan


class TestStudyPlanner(unittest.TestCase):
    def test_low_energy_short_time_hard_task(self):
        plan = infer_study_plan(energy=2.0, hours_available=1.0, complexity=8.0)
        self.assertLessEqual(plan["session_length_hours"], 1.0)
        self.assertLess(plan["focus_percentage"], 70.0)
        self.assertGreaterEqual(plan["rest_minutes"], 25.0)

    def test_high_energy_long_time_easy_task(self):
        plan = infer_study_plan(energy=9.0, hours_available=6.0, complexity=2.0)
        self.assertGreaterEqual(plan["session_length_hours"], 2.5)
        self.assertGreaterEqual(plan["focus_percentage"], 80.0)
        self.assertLess(plan["rest_minutes"], 25.0)


if __name__ == "__main__":
    unittest.main()
