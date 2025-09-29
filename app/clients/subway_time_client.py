import itertools
import time
from typing import Dict, Iterator, List, Optional, Union

import requests

StrOrList = Union[str, List[str]]


class SubwayTimeClient:
    DATA_TYPE = "JSON"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout=10,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.session()

    def _norm(self, v: StrOrList) -> List[str]:
        if isinstance(v, str):
            return [v]
        return v

    def _one_call(
        self,
        pageNo: int,
        numOfRows: int,
        tmprTmtblYn: Optional[str],
        upbdnbSe: Optional[str],
        wkndSe: Optional[str],
        lineNm: Optional[str],
    ) -> Dict:
        url = f"{self.base_url}/getTrainSch"
        params = {
            "serviceKey": self.api_key,
            "pageNo": pageNo,
            "numOfRows": numOfRows,
            "tmprTmtblYn": tmprTmtblYn,
            "upbdnbSe": upbdnbSe,
            "wkndSe": wkndSe,
            "lineNm": lineNm,
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

        return data["response"]["body"]["items"].get("item", [])

    def fetch_timetable(
        self,
        line_list: Optional[StrOrList] = None,
    ) -> Iterator[Dict]:
        pageNo: int = 1
        numOfRows: int = 1000

        tmpr_list = self._norm(["Y", "N"])
        updn_list = self._norm(["상행", "하행", "내선", "외선"])
        week_list = self._norm(["평일", "주말", "공휴일", "상시"])
        line_list = self._norm(line_list)

        for tmpr, updn, week, line in itertools.product(
            tmpr_list, updn_list, week_list, line_list
        ):
            p = pageNo
            while True:
                items = self._one_call(
                    pageNo=p,
                    numOfRows=numOfRows,
                    tmprTmtblYn=tmpr,
                    upbdnbSe=updn,
                    wkndSe=week,
                    lineNm=line,
                )
                if not items:
                    break

                for it in items:
                    yield it

                if len(items) < numOfRows:
                    break

                p += 1
                time.sleep(0.15)
