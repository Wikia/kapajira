import hashlib

from datetime import datetime


class Issue:
    """This class is a simple wrapper for JIRA issue"""

    DESCRIPTION_HASH_FORMAT = '\n\n========================\nHash: {hash}'
    LAST_OCCURRENCE_FORMAT = '\nLast Occurrence: {occurrence} UTC'

    def __init__(self, alert_id, description, issue_type='Defect', issue_component=None,
                 alert_name=None, labels=None):
        """ Set up the jira issue """
        self._alert_id = alert_id
        self._description = description
        self._issue_type = {
            'name': issue_type
        }
        self._issue_component = issue_component
        self._alert_name = alert_name
        self._issue_hash = self._create_hash(
            self.get_summary() + self._description.strip().split()[0])
        self._labels = ["KapacitorAlert"]
        if labels is not None:
            self._labels += labels

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
        if self._issue_component and self._alert_name:
            summary = self._alert_name + "/" + self._issue_component
        else:
            # prevent jira.exceptions.JIRAError:
            # HTTP 400: "The summary is invalid because it contains newline characters."
            summary = self._alert_id.replace("\n", '')

        # Max length of summary 255 characters
        return ("Kap Alert: " + summary)[:255]

    def get_description(self):
        """ Get report detailed description """
        description = self._description.strip()
        description += self.DESCRIPTION_HASH_FORMAT.format(hash=self._issue_hash)
        description += self.LAST_OCCURRENCE_FORMAT.format(occurrence=datetime.utcnow())
        return description

    def get_labels(self):
        """ Get a list of labels """
        return self._labels

    def get_component(self):
        return self._issue_component
