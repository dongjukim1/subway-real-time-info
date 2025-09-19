from typing import Any, Dict, List

import requests


class SubwayInfoClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        data_type: str,
        api_name: str,
        start_index: int,
        end_index: int,
        timeout=10,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.data_type = data_type
        self.api_name = api_name
        self.start_index = start_index
        self.end_index = end_index
        self.timeout = timeout

    def fetch_infos(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/{self.api_key}/{self.data_type}/{self.api_name}/{self.start_index}/{self.end_index}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["SearchSTNBySubwayLineInfo"].get("row", [])
