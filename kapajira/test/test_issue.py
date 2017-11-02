import unittest

from kapajira.jira.issues import Issue


class TestIssue(unittest.TestCase):
    def test_hash(self):
        first = Issue("TRAEFIK_APDEX/Pandora", "TRAEFIK_APDEX/kube-sjc-prod/user-preference/user-preference-read \
        Apdex value 0.9285714285714286 below configured threshold: 0.95 \
        Find out more: https://metrics.wikia-inc.com/dashboard/db/traefik-apdex")
        second = Issue("TRAEFIK_APDEX/Pandora", "TRAEFIK_APDEX/kube-sjc-prod/geoip/ \
        Apdex value 0.9861111111111112 below configured threshold: 0.99 \
        Find out more: https://metrics.wikia-inc.com/dashboard/db/traefik-apdex")

        self.assertNotEqual(first.get_issue_hash(), second.get_issue_hash(),
                            "Hash should be different for different services")
