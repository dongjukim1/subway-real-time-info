import re
from datetime import datetime, timezone

NULLS = {"", "NULL", "None", "NONE"}


def to_list(v, sep_pattern=r"[,\|/;\s]+"):
    if v is None:
        return []
    vals = v if isinstance(v, list) else re.split(sep_pattern, str(v))
    out, seen = [], set()
    for s in (x.strip() for x in vals):
        if not s or s in seen or s.upper() in NULLS:
            continue
        seen.add(s)
        out.append(s)
    return out


def normalize_alert_item(item: dict) -> dict:
    line_names = to_list(item.get("lineNmLst"))
    station_ids = to_list(item.get("stnSctnCdLst"))
    doc = {
        "title": item.get("noftTtl"),
        "description": item.get("noftCn"),
        "event_time": item.get("noftOcrnDt"),
        "line_name": line_names,
        "station_id": station_ids,
        "event_type": item.get("noftSeCd"),
        "nonstop": item.get("nonstopYn"),
        "direction": item.get("upbdnbSe"),
        "incident_start": item.get("xcseSitnBgngDt"),
        "incident_end": item.get("xcseSitnEndDt"),
        "create_Ymd": item.get("crtrYmd"),
        "create_time": datetime.now(timezone.utc).isoformat(),
        "_raw": {
            "stnSctnCdLst": item.get("stnSctnCdLst"),
            "lineNmLst": item.get("lineNmLst"),
        },
    }
    return doc


def explode_by_station(doc: dict) -> list[dict]:
    sids = doc.get("station_id", [])
    if not sids:
        return [doc]
    out = []
    for sid in sids:
        d = {**doc, "station_id": sid}
        out.append(d)
    return out


def make_doc_id(d: dict) -> str:
    et = (d.get("event_time") or "").replace(" ", "T")
    sid = d.get("station_id") or "NO_STATION"
    return f"{et}_{sid}"
