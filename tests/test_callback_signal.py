from examples.with_signals import app, my_signal

from ._utils import CustomTestCase


class TestCallbackAndSignal(CustomTestCase):
    uri = "/cmd/echo"

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_callback_fn_gets_called(self):
        self.signal_was_called = False

        @my_signal.connect
        def handler(sender, **kwargs):
            self.signal_was_called = True

        data = {"args": ["hello", "world"]}
        # make request
        r1 = self.client.post(self.uri, json=data)
        # fetch report
        _ = self.fetch_result(r1.json["key"])
        self.assertTrue(self.signal_was_called)
