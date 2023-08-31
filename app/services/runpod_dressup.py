from typing import Optional

import requests

from app.schemas import OrderWithData, RunpodResponse


class RunpodDressUpService(object):
    def __init__(self, api_url: str, api_token: str) -> None:
        self._api_url = api_url
        self._session = requests.Session()

        self._session.headers.update({
            "Authorization": f"Bearer {api_token}"
        })

    def _send_request(self, method: str, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None) -> dict:
        url = f"{self._api_url}{endpoint}"
        print("URL", url)
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json
        )
        response.raise_for_status()
        return response.json()

    def wakeup(self, order: OrderWithData) -> RunpodResponse | None:
        body = {
            "id": "",
            "input": {
                "order": order.model_dump()
            }
        }

        try:
            res = self._send_request(
                method="POST",
                endpoint="/",
                json=body
            )
            print(res)
            runpod_response = RunpodResponse(**res)
            return runpod_response
        except requests.exceptions.HTTPError as e:
            print(e)
            return None
