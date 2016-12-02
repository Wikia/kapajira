import hashlib


class Issue:
    """This class is a simple wrapper for JIRA issue"""

    DESCRIPTION_HASH_FORMAT = '\n\n========================\nHash: {hash}'

    def __init__(self, summary, description, issue_type='Defect'):
        """ Set up the jira issue """
        self._summary = summary
        self._description = description
        self._issue_type = {
            'name': issue_type
        }
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
        return self._summary.replace("\n", '')

    def get_description(self):
        """ Get report detailed description """
        description = self._description.strip()
        description += self.DESCRIPTION_HASH_FORMAT.format(hash=self._issue_hash)
        return description
