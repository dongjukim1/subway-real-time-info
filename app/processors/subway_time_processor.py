import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def _split_hms(
    hms: Optional[str],
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if not hms:
        return None, None, None
    try:
        h, m, s = map(int, hms.split(":"))
        return h, m, s
    except Exception:
        return None, None, None


def build_datetime(hms: Optional[str], ymd: str = "20250901") -> Optional[str]:
    h, m, s = _split_hms(hms)
    if h is None:
        return None
    base = datetime.strptime(ymd, "%Y%m%d")
    dt = base + timedelta(hours=h, minutes=m, seconds=s)
    return dt.strftime("%Y%m%d%H%M%S")


def normalize_time(item: dict) -> dict | None:
    raw_hms = item.get("trainDptreTm")  # 'HH:mm:ss'
    subway_time = build_datetime(raw_hms)  # 'yyyyMMddHHmmss'
    if subway_time is None:
        return None

    doc = {
        "station_name": {"ko": item.get("stnNm")},  # station name
        "express_train": item.get("etrnYn"),  # express train [y,n]
        "subway_time": subway_time,  # subway begin time dd
        "up_and_down": item.get("upbdnbSe"),  # up and down
        "wkndSe": item.get("wkndSe"),  #  weekend
        "line_name": item.get("lineNm"),  # line name
        "station_id": item.get("stnCd"),  # station id
        "station_fr_id": item.get("stnNo"),  # station fr id
        "subway_no": item.get("trainno"),  # subway number
        "dptreStnCd": item.get("dptreStnCd"),  # subway start station id
        "dptreStnNo": item.get("dptreStnNo"),  # subway start station fr id
        "dptreStnNm": item.get("dptreStnNm"),  # subway start station name ko
        "arvlStnCd": item.get("arvlStnCd"),  # subway end station id
        "arvlStnNo": item.get("arvlStnNo"),  # subway end station fr id
        "arvlStnNm": item.get("arvlStnNm"),  # subway end station name ko
        "dptreLineNm": item.get("dptreLineNm"),  # subway start line name
        "arvlLineNm": item.get("arvlLineNm"),  # subwway end line name
        "brlnNm": item.get("brlnNm"),  #
        "trainArvlTm": build_datetime(
            item.get("trainArvlTm")
        ),  # subway now station arrival time   dd
        "trainKnd": item.get("trainKnd"),  # subway kind
        "lnkgTrainno": item.get("lnkgTrainno"),  #
        "tmprTmtblYn": item.get("tmprTmtblYn"),  #
        "vldBgngDt": item.get("vldBgngDt"),  #
        "vldEndDt": item.get("vldEndDt"),  #
        "updated_at": item.get("crtrYmd"),  # updated at
        "created_at": datetime.now(timezone.utc).isoformat(),  # es load time
    }
    return doc


def _slug(s) -> str:
    if s is None or s == "":
        return "na"
    s = str(s).strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^0-9a-z가-힣\-._]", "", s)
    return s or "na"


def make_doc_id(d: dict) -> str:
    sid1 = _slug(d.get("line_name"))
    sid2 = _slug(d.get("wkndSe"))
    sid3 = _slug(d.get("up_and_down"))
    sid4 = _slug(d.get("station_id"))
    sid5 = _slug(d.get("subway_time"))

    return f"{sid1}_{sid2}_{sid3}_{sid4}_{sid5}"
