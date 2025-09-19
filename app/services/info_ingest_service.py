from app.clients.subway_info_client import SubwayInfoClient
from app.processors.subway_info_processor import make_doc_id, normalize_info_item
from app.repositories.es_repository import ESRepo


class InfoIngestService:
    def __init__(self, client: SubwayInfoClient, es: ESRepo, index: str):
        self.client = client
        self.es = es
        self.index = index

    def run_once(self):
        raw_items = self.client.fetch_infos()
        docs = []
        for it in raw_items:
            base = normalize_info_item(it)
            docs.append(base)
        self.es.bulk_index(self.index, docs, id_func=make_doc_id)
