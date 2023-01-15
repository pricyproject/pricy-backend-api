
from typing import Any, Dict, List
from django.conf import settings
import meilisearch
from meilisearch.index import Index


class SearchIndex():
    client: meilisearch.Client = None
    index_uid: str = None

    def __init__(self, index_uid) -> None:
        self.client = meilisearch.Client(
            settings.MEILISEARCH_URL, settings.MEILISEARCH_MASTER_KEY)
        self.index_uid = index_uid

    def get_index(self) -> Index:
        return self.client.index(self.index_uid)

    def create_index(self, name: str) -> None:
        self.client.create_index(name)

    def raw_search(self, query: str) -> List[Dict[str, Any]]:
        return self.get_index().search(query)['hits']

    def search(self, query: str, limit=10, offset=0) -> list:
        index = self.get_index()
        primary_key = index.get_primary_key()

        if not primary_key:
            raise Exception(f"Unable find primary key for '{index.uid}' index")

        search_result = index.search(query, {'limit': limit, 'offset': offset})

        hit_keys = []

        for hit in search_result.get('hits'):
            hit_keys.append(hit[primary_key])

        return hit_keys


class SearchIndexNames:
    product_groups = "product_groups"
