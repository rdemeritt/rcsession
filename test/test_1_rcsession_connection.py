from unittest import TestCase
from rcsession import rcsession
from rcsession.rd_utilities import get_json_file_contents


class TestRCSessionConnection(TestCase):
    token = None

    def test_1_force_failure(self):
        # ensure we are not connected already
        session = rcsession.RCSession(_key='force failure')
        self.assertFalse(session.get_token())
        self.assertTrue(session.close_requests())

    def test_2_api_connection(self):
        # test api_gw connection auth from file
        # session = rcsession.RCSession(_key=TestRCSessionConnection.api_gw_key['key'])
        session = rcsession.RCSession(_key='rcsession/test/key.json')
        self.assertTrue(session.get_token())
        # close our api_gw connection
        self.assertTrue(session.close_requests())

        # test api_gw connection direct key
        # set api_gw_key
        api_gw_key = get_json_file_contents('rcsession/test/key.json')['key']
        session = rcsession.RCSession(_key=api_gw_key)
        self.assertTrue(session.get_token())
        # get a token for our next test
        TestRCSessionConnection.token = session.get_token()['serialized']
        # close our api_gw connection
        self.assertTrue(session.close_requests())

    def test_3_token_connection(self):
        # test token connection
        session = rcsession.RCSession(_token=TestRCSessionConnection.token)
        self.assertTrue(session.get_token())

        # close our token connection
        self.assertTrue(session.close_requests())
