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

    fr = (item.get("FR_CODE") or "").strip()
    fr_norm = norm_code(fr) if fr else None

    tokens = name_values[:]
    if fr:
        tokens.append(fr)
    if fr_norm:
        tokens.append(fr_norm)

    station_search = list(dict.fromkeys(tokens))

    doc = {
        "station_id": item.get("STATION_CD"),  # station id
        "station_name": names_obj,  # station name [ko, en, cn, jp]
        "line_name": line_name,  # line name
        "station_fr_id": fr,  # station fr id
        "station_fr_id_norm": fr_norm,  # station fr id norm
        "station_search": station_search,  # es search set
        "created_at": datetime.now(timezone.utc).isoformat(),  # es load time
        "_raw": {"LINE_NUM": item.get("LINE_NUM")},
    }

    return doc


def make_doc_id(d: dict) -> str:
    return d.get("station_id")
