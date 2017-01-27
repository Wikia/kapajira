from jira import JIRA

from kapajira.config import JIRA_CONFIG as CFG


class JiraReporter:
    """Main interface for creating and searching issues on JIRA"""

    JQL_NOT_IN_STATUS = "status != '{status}'"
    JQL_DESCRIPTION_CONTAINS = "description ~ '{hash_value}'"

    STATUS_CLOSED = 'Closed'
    STATUS_OPEN = 'Open'

    def __init__(self):
        self._project = CFG['project']
        self._jira = JIRA(server=CFG['url'],
                          basic_auth=(CFG['user'], CFG['password']))

    def issue_exists(self, issue_hash: str):
        """Checks if JIRA issues with issue_hash in description exists.

        Searches for 'Open' JIRA issues which contains issue_hash in their
        description.

        Args:
            issue_hash: hash that will be searched in JIRA description field

        Returns:
            first JIRA issue which is not in status 'Closed'
            and contains issue_hash or None

        """
        issues = self._search_for_issues(issue_hash, self.STATUS_CLOSED)

        if issues is not None:
            return issues[0]
        else:
            return None


    def create_issue(self, issue):
        """Creates an JIRA issue or updates and existing one

        Creates JIRA issue at project taken from configuration file.

        Args:
            issue: an instance of kapajira.jira.Issue class

        """

        existing_issue = self.issue_exists(issue.get_issue_hash())

        issue_dict = {
            'project': self._project,
            'summary': issue.get_summary(),
            'description': issue.get_description(),
            'issuetype': issue.get_issue_type(),
            'labels': issue.get_labels()
        }

        if issue.get_component() is not None and self._component_exists(issue.get_component()):
            issue_dict['components'] = [{'name': issue.get_component()}]

        if existing_issue is not None:
            existing_issue.update(fields={'description' : issue_dict['description']})
        else:
            self._jira.create_issue(fields=issue_dict)

    def _search_for_issues(self, issue_hash, status):
        jql_query = ' AND '.join([
            self.JQL_DESCRIPTION_CONTAINS.format(hash_value=issue_hash),
            self.JQL_NOT_IN_STATUS.format(status=status)]
        )

        return self._jira.search_issues(jql_query)

    def _component_exists(self, component_name: str) -> bool:
        components_for_project = self._jira.project_components(project=self._project)
        for x in components_for_project:
            if component_name == x.name:
                return True
        return False
