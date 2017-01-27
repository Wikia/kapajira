import unittest

from unittest.mock import patch, Mock
from kapajira.jira.reporter import JiraReporter
from kapajira.jira.issues import Issue


class TestJiraReporter(unittest.TestCase):
    JIRA_SEARCH_STRING = "description ~ 'hash' AND status != 'Closed'"

    @patch('kapajira.jira.reporter.JIRA')
    def test_issue_exist_if_it_is_found(self, jira_mock):
        jira_mock = jira_mock.return_value
        jira_mock.search_issues.return_value = ['some_issue']
        jp = JiraReporter()

        self.assertTrue(jp.issue_exists('hash'))
        jira_mock.search_issues.assert_called_once_with(self.JIRA_SEARCH_STRING)

    @patch('kapajira.jira.reporter.JIRA')
    def test_issue_does_not_exist_if_it_is_not_found(self, jira_mock):
        jira_mock = jira_mock.return_value
        jira_mock.search_issues.return_value = []
        jp = JiraReporter()

        self.assertFalse(jp.issue_exists('hash'))
        jira_mock.search_issues.assert_called_once_with(self.JIRA_SEARCH_STRING)

    @patch('kapajira.jira.reporter.JIRA')
    def test_issue_is_created_if_one_does_not_exist(self, jira_mock):
        jira_mock = jira_mock.return_value
        jira_mock.search_issues.return_value = []

        jp = JiraReporter()

        issue_mock = Mock(spec=Issue)
        issue_mock.get_description.return_value = 'some_desc'
        issue_mock.get_issue_hash.return_value = 'some_hash'

        jp.create_issue(issue_mock)

    @patch('kapajira.jira.reporter.JIRA')
    def test_issue_is_not_created_if_one_exist(self, jira_mock):
        jira_issue_mock = Mock()

        jira_mock = jira_mock.return_value
        jira_mock.search_issues.return_value = [jira_issue_mock]

        jp = JiraReporter()
        issue_mock = Mock(spec=Issue)
        issue_mock.get_description.return_value = 'some_desc'

        jp.create_issue(issue_mock)
        jira_issue_mock.update.assert_called_once_with(fields={'description': 'some_desc'})
