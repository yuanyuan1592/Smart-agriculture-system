import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.modules.weather.service import WeatherModuleService


class WeatherServiceTest(unittest.TestCase):
    def test_weather_service_returns_weather_info(self):
        report = WeatherModuleService.get_weather()

        self.assertIn("generated_at", report)
        self.assertIn("weather", report)
        self.assertIsInstance(report["weather"], list)
        self.assertGreater(len(report["weather"]), 0)

        first = report["weather"][0]
        self.assertIn("location", first)
        self.assertIn("temperature", first)
        self.assertIn("humidity", first)
        self.assertIn("wind_direction", first)
        self.assertIn("wind_strength", first)
        self.assertIn("air_quality", first)
        self.assertIn("aqi", first)
        self.assertIn("uv_index", first)
        self.assertIn("forecast", first)
        self.assertIn("disaster_predictions", first)
        self.assertIsInstance(first["forecast"], list)
        self.assertIsInstance(first["disaster_predictions"], list)


if __name__ == "__main__":
    unittest.main()
