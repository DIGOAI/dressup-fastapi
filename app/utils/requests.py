import requests


class APIRequester:
    """A client for making requests."""

    def __init__(self, base_url: str, bearer_token: str):
        self.base_url = base_url
        self.bearer_token = bearer_token
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {bearer_token}"})

    def send_request(
        self,
        method="POST",
        endpoint="/",
        params=None,
        json: dict = None,
        timeout: int = 100,
    ):
        """Make a request using session data."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method, url, params=params, json=json, timeout=timeout
        )
        response.raise_for_status()
        return response.json()
