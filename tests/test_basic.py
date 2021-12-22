import time

from examples.basic import app, shell2http

from tests._utils import CustomTestCase, post_req_keys, get_req_keys


class TestBasic(CustomTestCase):
    uri = "/cmd/echo"

    def create_app(self):
        app.config["TESTING"] = True
        shell2http.register_command(endpoint="sleep", command_name="sleep")
        return app

    def test_keys_and_basic_sanity(self):
        # make request
        r1 = self.client.post(self.uri, json={"args": ["hello", "world"]})
        self.assertStatus(r1, 202)
        r1_json = r1.get_json()
        for k in post_req_keys:
            self.assertIn(k, r1_json)
        # fetch result
        r2 = self.fetch_result(r1_json["key"])
        self.assertStatus(r2, 200)
        r2_json = r2.get_json()
        for k in get_req_keys:
            self.assertIn(k, r2_json)
        self.assertEqual(r2_json["key"], r1_json["key"])
        self.assertEqual(r2_json["report"], "hello world\n")
        self.assertEqual(r2_json["returncode"], 0)
        self.assertEqual(
            r2_json["process_time"], r2_json["end_time"] - r2_json["start_time"]
        )

    def test_timeout_raises_error(self):
        # make request
        # timeout in seconds, default value is 3600
        r1 = self.client.post("/cmd/sleep", json={"args": ["5"], "timeout": 1})
        self.assertStatus(r1, 202)
        r1_json = r1.get_json()
        # sleep for sometime
        time.sleep(2)
        # fetch result
        r2 = self.fetch_result(r1_json["key"])
        self.assertStatus(r2, 200)
        r2_json = r2.get_json()
        print(r2_json)
        self.assertEqual(r2_json["key"], r1_json["key"])
        self.assertEqual(r2_json["report"], "")
        self.assertEqual(r2_json["error"], "command timedout after 1 seconds.")
        self.assertEqual(r2_json["returncode"], -9)

    def test_duplicate_request_raises_error(self):
        data = {"args": ["test_duplicate_request_raises_error"]}
        _ = self.client.post(self.uri, json=data)
        r2 = self.client.post(self.uri, json=data)
        self.assertStatus(
            r2, 400, message="future key would already exist thus bad request"
        )
        r2_json = r2.get_json()
        self.assertIn("error", r2_json)
        self.assertIn("key", r2_json)
        self.assertIn("result_url", r2_json)

    def test_duplicate_request_after_report_fetch(self):
        data = {"args": ["test_duplicate_request_after_report_fetch"]}
        # make 1st request
        r1 = self.client.post(self.uri, json=data)
        r1_json = r1.get_json()
        # wait for initial request to complete
        _ = self.fetch_result(r1_json["key"])
        # now make 2nd request
        r2 = self.client.post(self.uri, json=data)
        r2_json = r2.get_json()
        # should have same response
        self.assertDictEqual(r2_json, r1_json)

    def test_force_unique_key(self):
        data = {"args": ["test_force_unique_key"]}
        r1 = self.client.post(self.uri, json=data)
        r1_json = r1.get_json()
        r2 = self.client.post(self.uri, json={**data, "force_unique_key": True})
        r2_json = r2.get_json()
        self.assertNotEqual(r2_json["key"], r1_json["key"])

    def test_get_with_wait(self):
        # 1. POST request
        r1 = self.client.post("/cmd/sleep", json={"args": ["2"]})
        r1_json = r1.get_json()
        # 2. GET request with wait=True
        r2 = self.client.get(r1_json["result_url"].replace("false", "true"))
        r2_json = r2.get_json()
        # 3. asserts
        self.assertEqual(r2_json["key"], r1_json["key"])
        self.assertEqual(r2_json["report"], "")
        self.assertEqual(r2_json["error"], "")
        self.assertEqual(r2_json["returncode"], 0)
