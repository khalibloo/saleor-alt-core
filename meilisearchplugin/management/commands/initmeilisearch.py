import logging
from typing import Dict

from django.core.management.base import BaseCommand
from meilisearch.errors import MeiliSearchError

from saleor.product.models import Product
from ...tasks import add_or_replace_documents
from ...utils import serialize_product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate thumbnails for all images"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("url", nargs=1, help="Your MeiliSearch server URL")

        # Named (optional) arguments
        parser.add_argument(
            "--apikey", help="Your API Key if your MeiliSearch server uses one",
        )

    def handle(self, *args, **options):
        config = {
            "meilisearch_url": options.get("url")[0],
            "api_key": options.get("apikey", None),
        }
        self.create_products_index(config)

    def create_products_index(self, config: Dict):
        self.stdout.write("Serializing products")
        docs = []
        products = Product.objects.filter()
        for p in products:
            if p.is_visible and p.is_available_for_purchase:
                # self.stdout.write("Product ID: " + str(p.id))
                docs.append(serialize_product(p))
            else:
                self.stdout.write(
                    "Skipping Product ID (product unavailable): " + str(p.id)
                )
        try:
            add_or_replace_documents(config, "products", docs, clear=True)
        except MeiliSearchError as err:
            self.stderr.write(err.message)
        self.stdout.write("Finished creating products index")
        self.stdout.write("Happy Searching!")
