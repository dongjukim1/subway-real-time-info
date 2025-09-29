from datetime import datetime, timezone


def normalize_fast_exit_item(item: dict) -> dict:
    doc = {
        "fast_info_id": item.get("qckgffMngNo"),  # fast_info_id
        "line_name": item.get("lineNm"),  # line name
        "station_id": item.get("stnCd"),  # station id
        "station_name": {"ko": item.get("stnNm")},  # station name [ko]
        "station_fr_id": item.get("stnNo"),  # station fr id
        "up_and_down": item.get("upbdnbSe"),  # up and down
        "next_station": item.get("drtnInfo"),  # next station
        "fast_exit_door": item.get("qckgffVhclDoorNo"),  # fast exit door
        "fac_name": item.get("plfmCmgFac"),  # Facilities name
        "fac_loc_1": item.get("facPstnNm"),  # Facilities station loc
        "fac_loc_2": item.get("fwkPstnNm"),  # Facilities station addr
        "fac_no": item.get("facNo"),  # Facilities num
        "elvtr_no": item.get("elvtrNo"),  # elvtrNo
        "updated_at": item.get("crtrYmd"),  #  last updated
        "created_at": datetime.now(timezone.utc).isoformat(),  # es load time
    }
    return doc


def make_doc_id(d: dict) -> str:
    sid = d.get("station_id") or "NO_STATION"
    exit = d.get("fast_info_id") or "NO_EXIT"

    return f"{sid}_{exit}"
