from jira import JIRA

from kapajira.config import JIRA_CONFIG as CFG


class JiraReporter:
    """Main interface for creating and searching issues on JIRA"""

    JQL_OPEN_STATUS = "status = '{status}'"
    JQL_DESCRIPTION_CONTAINS = "description ~ '{hash_value}'"

    STATUS_CLOSED = 'Closed'
    STATUS_OPEN = 'Open'

    def __init__(self):
        self._project = CFG['project']
        self._jira = JIRA(server=CFG['url'],
                          basic_auth=(CFG['user'], CFG['password']))

    def issue_exists(self, issue_hash: str) -> list:
        """Checks if JIRA issues with issue_hash in description exists.

        Searches for 'Open' JIRA issues which contains issue_hash in their
        description.

        Args:
            issue_hash: hash that will be searched in JIRA description field

        Returns:
            True if there is at least one JIRA issue which is 'Open'
            and contains issue_hash, False otherwise

        """
        issues = self._search_for_issues(issue_hash, self.STATUS_OPEN)

        return True if issues else False

    def create_issue(self, issue):
        """Creates an JIRA issue

        Creates JIRA issue at project taken from configuration file.

        Args:
            issue: an instance of kapajira.jira.Issue class

        Returns:
            None if no issue was created. Otherwise return new issue id

        """

        if self.issue_exists(issue.get_issue_hash()):
            return

        issue_dict = {
            'project': self._project,
            'summary': issue.get_summary(),
            'description': issue.get_description(),
            'issuetype': issue.get_issue_type()
        }

        if issue.get_component() is not None:
            issue_dict['components'] = [{'name': issue.get_component()}]

        return self._jira.create_issue(fields=issue_dict)

    def _search_for_issues(self, issue_hash, status):
        jql_query = ' AND '.join([
            self.JQL_DESCRIPTION_CONTAINS.format(hash_value=issue_hash),
            self.JQL_OPEN_STATUS.format(status=status)]
        )

        return self._jira.search_issues(jql_query)
