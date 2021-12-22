from examples.deletion import app

from tests._utils import CustomTestCase


class TestDeletion(CustomTestCase):
    uri = "/sleep"

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_delete__204(self):
        # create command process
        r1 = self.client.post(self.uri, json={"args": ["10"], "force_unique_key": True})
        r1_json = r1.get_json()
        self.assertStatus(r1, 202)
        # request cancellation: correct key
        r2 = self.client.delete(f"{self.uri}?key={r1_json['key']}")
        self.assertStatus(r2, 204)

    def test_delete__400(self):
        # create command process
        r1 = self.client.post(self.uri, json={"args": ["10"], "force_unique_key": True})
        self.assertStatus(r1, 202)
        # request cancellation: no key
        r2 = self.client.delete(f"{self.uri}?key=")
        self.assertStatus(r2, 400)

    def test_delete__404(self):
        # create command process
        r1 = self.client.post(self.uri, json={"args": ["10"], "force_unique_key": True})
        self.assertStatus(r1, 202)
        # request cancellation: invalid key
        r2 = self.client.delete(f"{self.uri}?key=abcdefg")
        self.assertStatus(r2, 404)
