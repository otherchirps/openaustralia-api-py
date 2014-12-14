import unittest
import requests_mock

from openaustralia import api


class TestApi(unittest.TestCase):

    def setUp(self):
        self.test_key = "123123"

        self.api = api.OpenAustralia(
            self.test_key
        )

    def tearDown(self):
        self.api = None

    def _check_api_function_called(
        self, expected_api_function, test_call,
        *args, **kwargs
    ):
        """ Helper function.

        Calls the given `test_call`, and confirms whether
        the correct `api_function` request was sent (via the mock).

        Common boiler-plate check that we'll want for every
        method we offer.
        """
        function_path = "/" + expected_api_function

        # Seems that requests lower-cases the paths?
        expected_function_path = '/api' + function_path.lower()

        with requests_mock.Mocker() as m:
            m.register_uri(
                "GET",
                api.API_BASE_URL + function_path,
                json=[{'akey': 'stuff'}]
            )
            result = test_call(*args, **kwargs)
            self.assertIsNotNone(result)
            self.assertEqual(
                expected_function_path,
                m.last_request.path
            )
            self.assertEqual(result[0]['akey'], 'stuff')

    def test_api_key_sent(self):
        with requests_mock.Mocker() as m:
            # Just calling any api function.
            # not interested in its result here.
            m.register_uri(
                "GET",
                api.API_BASE_URL + "/getDivisions",
                json=[{'division1': 'stuff'}]
            )
            self.api.get_divisions('2010')

            # Want to check the request layer -
            # Did we send anything (to the mock)?
            # Did our key get passed along?
            self.assertTrue(m.last_request)
            request_params = m.last_request.qs
            self.assertTrue('key' in request_params)
            self.assertTrue(
                self.test_key in request_params['key'],
            )

    def test_get_divisions(self):
        self._check_api_function_called(
            'getDivisions',
            self.api.get_divisions,
            postcode='2010'
        )

    def test_get_representative(self):
        self._check_api_function_called(
            'getRepresentative',
            self.api.get_representative,
            person_id=123
        )

    def test_get_representatives(self):
        self._check_api_function_called(
            'getRepresentatives',
            self.api.get_representatives,
            postcode='2010'
        )

    def test_get_senator(self):
        self._check_api_function_called(
            'getSenator',
            self.api.get_senator,
            person_id=123
        )

    def test_get_senators(self):
        self._check_api_function_called(
            'getSenators',
            self.api.get_senators,
            state="NSW"
        )

    def test_get_debates(self):
        self._check_api_function_called(
            'getDebates',
            self.api.get_debates,
            debate_type='senate',
            search='foo'
        )

    def test_get_hansard(self):
        self._check_api_function_called(
            'getHansard',
            self.api.get_hansard,
            search='foo'
        )

    def test_get_comments(self):
        self._check_api_function_called(
            'getComments',
            self.api.get_comments
        )
