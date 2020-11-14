from typing import Dict, List

from celery import shared_task
import meilisearch

@shared_task
def add_or_replace_documents(
    config: Dict, index: str, docs: List[Dict], clear: bool = False
):
    print("creating client")
    client = meilisearch.Client(
        config["meilisearch_url"], apiKey=config.get("api_key", None)
    )
    if clear:
        print("clearing existing index, if it exists")
        client.get_or_create_index(index).delete()
    print("adding or replacing documents in index")
    client.get_or_create_index(index).add_documents(docs)
