from typing import Any, Dict, List

import requests


class SubwayInfoClient:
    API_NAME = "SearchSTNBySubwayLineInfo"
    DATA_TYPE = "JSON"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        start_index: int,
        end_index: int,
        timeout=10,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.start_index = start_index
        self.end_index = end_index
        self.timeout = timeout

    def fetch_infos(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{self.api_key}/{self.DATA_TYPE}/{self.API_NAME}/{self.start_index}/{self.end_index}"

        try:
            response = requests.get(url)
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

        return data["SearchSTNBySubwayLineInfo"].get("row", [])
