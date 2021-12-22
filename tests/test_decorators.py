from examples.with_decorators import app

from tests._utils import CustomTestCase


class TestDecorators(CustomTestCase):
    public_uri = "/cmd/public/echo"
    private_uri = "/cmd/protected/echo"
    uri = public_uri  # default

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_decorators(self):
        data = {"args": ["hello", "world"]}
        # make request
        r1 = self.client.post(self.public_uri, json=data)
        self.assertStatus(
            r1,
            202,
            message="202 status code because `login_required` decorator not applied",
        )
        r2 = self.client.post(self.private_uri, json=data)
        print(r1.json, r2.json)
        self.assertStatus(
            r2,
            401,
            message="401 status code because `login_required` decorator was applied",
        )
