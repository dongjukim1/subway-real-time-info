INDEX_DEFS = {
   "subway-alerts" : {
        "settings": {"number_of_shards": 1, "number_of_replicas": 1},
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "description": {"type": "text"},
                "event_time": {"type": "date", "format": "yyyyMMddHHmmss||strict_date_optional_time"},
                "line_name": {"type": "keyword"},
                "station_id":  {"type": "keyword"},
                "create_Ymd":   {"type": "text"},
                "event_type": {"type": "keyword"},
                "nonstop": {"type": "text"},
                "direction": {"type": "text"},
                "incident_start":  {"type": "date", "format": "yyyyMMddHHmmss||strict_date_optional_time"},
                "incident_end":  {"type": "date", "format": "yyyyMMddHHmmss||strict_date_optional_time"},
                "create_time" : {"type": "date", "format": "yyyyMMddHHmmss||strict_date_optional_time"}
            }
        }
    }
}
