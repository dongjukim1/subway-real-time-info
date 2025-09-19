from app.clients.subway_alert_client import SubwayAlertClient
from app.processors.subway_alert_processor import (
    explode_by_station,
    make_doc_id,
    normalize_alert_item,
)
from app.repositories.es_repository import ESRepo


class AlertIngestService:
    def __init__(self, client: SubwayAlertClient, es: ESRepo, index: str):
        self.client = client
        self.es = es
        self.index = index

    def run_once(self, start_ymd: str):
        raw_items = self.client.fetch_alerts(start_ymd)
        docs = []
        for it in raw_items:
            base = normalize_alert_item(it)
            docs.extend(explode_by_station(base))
        self.es.bulk_index(self.index, docs, id_func=make_doc_id)
