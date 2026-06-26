import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.registry import get_registered_routes
from app.routes import router  # noqa: F401


class RegistryTest(unittest.TestCase):
    def test_registered_routes_include_field_detection_and_analytics_modules(self):
        registrations = get_registered_routes()
        prefixes = [prefix for _, prefix, _ in registrations]

        self.assertIn("/api/fields", prefixes)
        self.assertIn("/api/detection", prefixes)
        self.assertIn("/api/analytics", prefixes)


if __name__ == "__main__":
    unittest.main()
