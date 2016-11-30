import unittest

from kapajira.kapacitor.utils import AlertDataParser


class TestAlertParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('resources/alert_data.json') as f:
            cls.ALERT_JSON_DATA = f.read()

    def setUp(self):
        self._alert_data = AlertDataParser.parse(TestAlertParser.ALERT_JSON_DATA)

    def test_alert_data_navigation(self):
        self.assertIn('HTTP_RESPONSE_TIME_HARD_SLA', self._alert_data.id)
        self.assertIn('alerting-tester', self._alert_data.message)
        self.assertEqual('CRITICAL', self._alert_data.level)
        self.assertEqual('2016-11-28T10:24:00Z', self._alert_data.time)


if __name__ == '__main__':
    unittest.main()
