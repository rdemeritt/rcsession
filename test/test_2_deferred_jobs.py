import json
from unittest import TestCase
from rcsession import rcsession


class TestDeferredJobs(TestCase):
    session = rcsession.RCSession(_key='rcsession/test/key.json')
    deferred_job = None

    def test_1_submit_deferred_job(self):
        # create search criteria
        hosts_search = {
            'domain': '%s' % 'd32c7944',
            'bulk': '%s' % 'true',
            'name': '%s_search_%s' % ('host', rcsession.rc_config.start_time)}

        # submit our search and ensure it's a bulk search
        response = TestDeferredJobs.session.get(TestDeferredJobs.session.hosts_url, params=hosts_search)
        # store for use later
        TestDeferredJobs.deferred_job = json.loads(response.text)
        # ensure we got a 200
        self.assertEqual(response.status_code, 200)

    def test_2_fetch_deferred_job(self):
        hosts_json = TestDeferredJobs.session.fetch_deferred_job(TestDeferredJobs.deferred_job['uuid'], _delete=False)
        self.assertIsNot(hosts_json, False)

    def test_3_delete_deferred_job(self):
        self.assertTrue(TestDeferredJobs.session.delete_deferred_job(TestDeferredJobs.deferred_job['uuid']))
        TestDeferredJobs.session.close_requests()
