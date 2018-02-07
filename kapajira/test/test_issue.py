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

    def test_multiple_instances_hash(self):
        first = Issue("HTTP_RESPONSE_5XX_RATE_BATCH/Pandora", "HTTP_RESPONSE_5XX_RATE_BATCH/sjc/static-assets/static-assets-7b497d78f8-4fdbx \
        The error rate (5xx responses) was above 0.05 at 0.20705882352941177 in the last 5m. \
        https://metrics.wikia-inc.com/dashboard/db/services-prod?var-serviceName=static-assets&var-resourceName=All&var-datacenter=sjc")
        second = Issue("HTTP_RESPONSE_5XX_RATE_BATCH/Pandora", "HTTP_RESPONSE_5XX_RATE_BATCH/sjc/static-assets/static-assets-7b497d78f8-5ndad \
        The error rate (5xx responses) was above 0.05 at 0.21 in the last 5m. \
        https://metrics.wikia-inc.com/dashboard/db/services-prod?var-serviceName=static-assets&var-resourceName=All&var-datacenter=sjc")

        self.assertEqual(first.get_issue_hash(), second.get_issue_hash(),
                         "Hash should be the same for different instances of the same service")

    def test_no_instance_hash(self):
        first = Issue("TRAEFIK_APDEX/Pandora", "TRAEFIK_APDEX/kube-sjc-prod/clickstream/clickstream \
        Apdex value 0.9876237623762376 below configured threshold: 0.99 \
        Find out more: https://metrics.wikia-inc.com/dashboard/db/traefik-apdex")
        second = Issue("TRAEFIK_APDEX/Pandora", "TRAEFIK_APDEX/kube-sjc-prod/clickstream/clickstream \
        Apdex value 0.9976237623762376 below configured threshold: 0.99 \
        Find out more: https://metrics.wikia-inc.com/dashboard/db/traefik-apdex")

        self.assertEqual(first.get_issue_hash(), second.get_issue_hash(),
                         "Hash should be the same for the same service")
