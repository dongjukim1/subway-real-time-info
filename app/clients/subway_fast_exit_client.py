import time
from typing import Any, Dict, List

import requests


class SubwayFastExitClient:
    DATA_TYPE = "JSON"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.session()

    def fetch_fast_exit(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/getFstExit"
        all_items: List[Dict[str, Any]] = []
        page = 1
        batch_size = 500
        while True:
            params = {
                "serviceKey": self.api_key,
                "pageNo": page,
                "numOfRows": batch_size,
                "dataType": self.DATA_TYPE,
            }

            try:
                response = self._session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
            except requests.Timeout:
                raise RuntimeError("Subway API request timed out.")
            except requests.ConnectionError:
                raise RuntimeError("Could not connect to the Subway API server.")
            except requests.HTTPError as e:
                raise RuntimeError(f"Subway API request failed: {e}") from e
            except requests.RequestException as e:
                raise RuntimeError(f"Subway API request error: {e}") from e
            except ValueError:
                raise RuntimeError("Subway API response is not valid JSON.")

            try:
                data = response.json()
            except ValueError:
                raise RuntimeError("Subway API response is not valid JSON.")

            items = (
                data.get("response", {})
                .get("body", {})
                .get("items", {})
                .get("item", [])
            )
            if not items:
                break

            all_items.extend(items)
            page += 1

            time.sleep(0.15)

            if len(items) < batch_size:
                break

        return all_items
