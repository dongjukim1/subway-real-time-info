import logging

from elasticsearch import Elasticsearch, helpers

logger = logging.getLogger(__name__)


class ESRepo:
    def __init__(self, host: str, timeout: int = 20):
        self.es = Elasticsearch(host, request_timeout=timeout)

    def ensure_index(self, name: str, body: dict):
        if self.es.indices.exists(index=name):
            logger.info("Index %s already exists", name)
            return
        self.es.indices.create(index=name, body=body)
        logger.info("Created index: %s", name)

    def ensure_all(self, index_defs: dict):
        for name, body in index_defs.items():
            self.ensure_index(name, body)

    def bulk_index(self, index: str, docs: list[dict], id_func) -> dict:
        actions = ({"_index": index, "_id": id_func(d), "_source": d} for d in docs)
        return helpers.bulk(self.es, actions, raise_on_error=False)
