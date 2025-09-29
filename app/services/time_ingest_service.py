from typing import Dict, Iterator, List, Optional, Union

from app.clients.subway_time_client import SubwayTimeClient
from app.processors.subway_time_processor import make_doc_id, normalize_time
from app.repositories.es_repository import ESRepo

StrOrList = Union[str, List[str]]


class SubwayTimeTableService:
    def __init__(self, client: SubwayTimeClient, es: ESRepo, index: str):
        self.client = client
        self.es = es
        self.index = index

    def run_once(self, line_list: Optional[StrOrList] = None):
        def docs():
            for it in self.client.fetch_timetable(line_list=line_list):
                doc = normalize_time(it)
                if doc is not None:
                    yield doc

        self.es.streaming_bulk_index(self.index, docs(), id_func=make_doc_id)
