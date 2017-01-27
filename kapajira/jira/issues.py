import hashlib
from datetime import datetime

class Issue:
    """This class is a simple wrapper for JIRA issue"""

    DESCRIPTION_HASH_FORMAT = '\n\n========================\nHash: {hash}'
    LAST_OCCURRENCE_FORMAT = '\nLast Occurrence: {occurrence} UTC'

    def __init__(self, summary, description, issue_type='Defect', issue_component=None):
        """ Set up the jira issue """
        self._summary = summary
        self._description = description
        self._issue_type = {
            'name': issue_type
        }
        self._issue_component = issue_component
        self._issue_hash = self._create_hash(summary)

    @staticmethod
    def _create_hash(data_to_hash):
        md5 = hashlib.md5()
        md5.update(data_to_hash.encode())
        return md5.hexdigest()

    def get_issue_type(self):
        """ Get jira issue type for this issue """
        return self._issue_type

    def get_issue_hash(self):
        """ Get the hash """
        return self._issue_hash

    def get_summary(self):
        """ Get issue summary """
        # prevent jira.exceptions.JIRAError:
        # HTTP 400: "The summary is invalid because it contains newline characters."
        return ("Kap Alert: " + self._summary.replace("\n", ''))[:255]

    def get_description(self):
        """ Get report detailed description """
        description = self._description.strip()
        description += self.DESCRIPTION_HASH_FORMAT.format(hash=self._issue_hash)
        description += self.LAST_OCCURRENCE_FORMAT.format(occurrence=datetime.utcnow())
        return description

    def get_labels(self):
        """ Get a list of labels """
        return ["KapacitorAlert"]

    def get_component(self):
        return self._issue_component
