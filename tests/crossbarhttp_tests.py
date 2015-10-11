import unittest
import crossbarhttp
import os

class CrossbarHttpTests(unittest.TestCase):

    url = None

    @classmethod
    def setUpClass(cls):
        cls.url = os.getenv('ROUTER_URL', "http://localhost:8080")

    def test_call(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertIsNotNone(publish_id)

    def test_call_no_callee(self):
        client = crossbarhttp.Client(self.__class__.url + "/call")

        with self.assertRaises(crossbarhttp.ClientNoCalleeRegistered) as context:
            client.call("test.does_not_exist", 2, 3, offset=10)

    def test_call_bad_url(self):
        client = crossbarhttp.Client(self.__class__.url + "/call_bad_url")

        with self.assertRaises(crossbarhttp.ClientBadUrl) as context:
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_url(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish_bad_url")

        with self.assertRaises(crossbarhttp.ClientBadUrl) as context:
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_bad_host(self):
        client = crossbarhttp.Client("http://bad:8080/call")

        with self.assertRaises(crossbarhttp.ClientBadHost) as context:
            client.call("test.add", 2, 3, offset=10)

    def test_publish_bad_host(self):
        client = crossbarhttp.Client("http://bad:8080/publish")

        with self.assertRaises(crossbarhttp.ClientBadHost) as context:
            client.publish("test.publish", 4, 7, event="new event")

    def test_call_missing_signature_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature")

        with self.assertRaises(crossbarhttp.ClientMissingParams) as context:
            client.call("test.add", 2, 3, offset=10)

    def test_call_bad_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(crossbarhttp.ClientSignatureError) as context:
            client.call("test.add", 2, 3, offset=10)

    def test_call_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/call-signature",
                                     key="key", secret="secret")
        result = client.call("test.add", 2, 3, offset=10)
        self.assertEqual(result, 15)

    def test_publish_missing_signature_params(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature")

        with self.assertRaises(crossbarhttp.ClientMissingParams) as context:
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_bad_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="bad secret")

        with self.assertRaises(crossbarhttp.ClientSignatureError) as context:
            client.publish("test.publish", 4, 7, event="new event")

    def test_publish_signature(self):
        client = crossbarhttp.Client(self.__class__.url + "/publish-signature",
                                     key="key", secret="secret")
        publish_id = client.publish("test.publish", 4, 7, event="new event")
        self.assertIsNotNone(publish_id)

    #def test_call_bad_parameters(self):
    #    client = Client(self.__class__.url + "/call", verbose=True)

    #    with self.assertRaises(Client.BadHost) as context:
    #        client.call("test.add", 2, 3, 4, 5, 6, offset=10)

    #def test_call_exception(self):
    #    client = Client(self.__class__.url + "/call", verbose=True)

    #    with self.assertRaises(Client.BadHost) as context:
    #        client.call("test.exception")


if __name__ == '__main__':
    unittest.main()
