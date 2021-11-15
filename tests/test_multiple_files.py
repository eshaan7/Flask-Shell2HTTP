import json
import io

from examples.multiple_files import app

from tests._utils import CustomTestCase


class TestMultipleFiles(CustomTestCase):
    uri = "/cmd/strings"

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_multiple_files(self):
        req_files = {
            "inputfile": (io.BytesIO(b"Test File #1"), "inputfile"),
            "someotherfile": (io.BytesIO(b"Test File #2"), "someotherfile"),
        }
        # the key should be `request_json` only.
        req_data = {
            "request_json": json.dumps({"args": ["@inputfile", "@someotherfile"]})
        }
        data = {**req_data, **req_files}
        # make request
        r1 = self.client.post(self.uri, data=data, content_type="multipart/form-data")
        key = r1.json["key"]
        r2 = self.fetch_result(key)
        r2_json = r2.get_json()
        self.assertEqual(r2_json["key"], key)
        self.assertEqual(r2_json["report"], "Test File #1\nTest File #2\n")
        self.assertEqual(r2_json["returncode"], 0)
