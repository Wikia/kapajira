"""
This script is intended to be invoked by kapacitor `exec` node.
It creates JIRA issue based on data passed in to STDIN from AlertNode.
"""
import sys

from kapajira.jira.reporter import JiraReporter
from kapajira.jira.issues import Issue
from kapajira.kapacitor.utils import AlertDataParser

alert_data = AlertDataParser.parse(sys.stdin.read())

if alert_data.level == 'CRITICAL':
    issue = Issue(alert_data.id, alert_data.message)
    reporter = JiraReporter()
    reporter.create_issue(issue)
