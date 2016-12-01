import unittest

from kapajira.kapacitor.utils import AlertDataParser


class TestAlertParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('resources/alert_data.json') as f:
            cls.ALERT_JSON_DATA = f.read()

    def setUp(self):
        self._alert_data = AlertDataParser.parse(TestAlertParser.ALERT_JSON_DATA)

    def test_simple_alert_data_navigation(self):
        self.assertIn('HTTP_RESPONSE_TIME_HARD_SLA', self._alert_data.id)
        self.assertIn('alerting-tester', self._alert_data.message)
        self.assertEqual('CRITICAL', self._alert_data.level)
        self.assertEqual('2016-11-28T10:24:00Z', self._alert_data.time)
        self.assertRaises(KeyError, lambda: self._alert_data.some_attribute)

    def test_deep_alert_data_navigation(self):
        self.assertEqual('resources', self._alert_data.data.series[0].name)
        self.assertEqual('alerting-tester', self._alert_data.data.series[0].tags.app)
        self.assertRaises(KeyError, lambda: self._alert_data.data.time)

    def test_adds_trailing_underscore_for_python_reserved_keyword_for_attribute(self):
        self.assertEqual('DEFECT', self._alert_data.class_)

    def test_cannot_change_alert_data_attributes(self):
        self.assertEqual('resources', self._alert_data.data.series[0].name)
        self.assertIsNotNone('resources', self._alert_data.data)

        with self.assertRaises(AttributeError) as err:
            self._alert_data.data.series = []
            self.assertEqual(err.msg, 'Attributes are read only')
            self.assertEqual('resources', self._alert_data.data.series[0].name)

        with self.assertRaises(AttributeError):
            self._alert_data.data = None
            self.assertEqual(err.msg, 'Attributes are read only')
            self.assertIsNotNone(self._alert_data.data)


if __name__ == '__main__':
    unittest.main()
