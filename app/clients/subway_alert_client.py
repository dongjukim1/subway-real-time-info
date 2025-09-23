from typing import Any, Dict, List

import requests


class SubwayAlertClient:
    DATA_TYPE = "JSON"

    def __init__(self, base_url: str, api_key: str, data_type: str, timeout=10):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.session()

    def fetch_alerts(self, start_ymd: str, rows: int = 100) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/getNtceList"
        params = {
            "serviceKey": self.api_key,
            "srchStartNoftOcrnYmd": start_ymd,
            "dataType": self.data_type,
            "numOfRows": rows,
        }
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.Timeout:
            raise RuntimeError("Subway API request timed out.")
        except requests.ConnectionError:
            raise RuntimeError("Could not connect to the Subway API server.")
        except requests.HTTPError as e:
            raise RuntimeError(f"Subway API request failed: {e}") from e
        except requests.RequestException as e:
            raise RuntimeError(f"Subway API request error: {e}") from e

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError("Subway API response is not valid JSON.")

        return data["response"]["body"]["items"].get("item", [])
