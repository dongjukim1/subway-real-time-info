from app.clients.subway_fast_exit_client import SubwayFastExitClient
from app.processors.subway_fast_exit_processor import (
    make_doc_id,
    normalize_fast_exit_item,
)
from app.repositories.es_repository import ESRepo


class SubwayFastExitService:
    def __init__(self, client: SubwayFastExitClient, es: ESRepo, index: str):
        self.client = client
        self.es = es
        self.index = index

    def run_once(self):
        raw_items = self.client.fetch_fast_exit()
        docs = []
        for it in raw_items:
            docs.append(normalize_fast_exit_item(it))
        self.es.bulk_index(self.index, docs, id_func=make_doc_id)
