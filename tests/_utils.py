import time

from flask_testing import TestCase

post_req_keys = ("key", "status", "result_url")

get_req_keys = (
    "end_time",
    "process_time",
    "error",
    "key",
    "report",
    "returncode",
    "start_time",
)


class CustomTestCase(TestCase):
    def fetch_result(self, key: str):
        uri = self.uri + f"?key={key}"
        running = True
        r = None
        while running:
            r = self.client.get(uri)
            status = r.json.get("status", None)
            if not status or status != "running":
                running = False
            # sleep a bit before next request
            time.sleep(0.5)
        return r
