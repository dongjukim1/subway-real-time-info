import re
from datetime import datetime, timezone


def normalize_line_name(raw_line: str) -> str:
    if raw_line:
        return raw_line.lstrip("0")
    return raw_line


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if not x or x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def norm_code(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalnum())


def normalize_info_item(item: dict) -> dict:
    names_obj = {
        "ko": item.get("STATION_NM"),
        "en": item.get("STATION_NM_ENG"),
        "cn": item.get("STATION_NM_CHN"),
        "jp": item.get("STATION_NM_JPN"),
    }
    name_values = [v.strip() for v in names_obj.values() if v and v.strip()]

    line_name = normalize_line_name(item.get("LINE_NUM"))

    fr = item.get("FR_CODE")
    codes = []

    if fr:
        fr_stripped = fr.strip()
        if fr_stripped:
            codes.append(fr_stripped)
            codes.append(fr_stripped.lower())
            codes.append(norm_code(fr_stripped))
        station_search = uniq(name_values + codes)

    doc = {
        "station_id": item.get("STATION_CD"),
        "station_name": names_obj,
        "line_name": line_name,
        "station_fr_code": uniq(codes),
        "station_search": station_search,
        "create_time": datetime.now(timezone.utc).isoformat(),
        "_raw": {"LINE_NUM": item.get("LINE_NUM")},
    }

    return doc


def make_doc_id(d: dict) -> str:
    return d.get("station_id")
