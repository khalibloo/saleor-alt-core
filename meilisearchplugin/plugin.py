from typing import Any

from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

from .utils import serialize_product
from .tasks import add_or_replace_documents


class MeiliSearchPlugin(BasePlugin):
    PLUGIN_ID = "khalibloo.meilisearch"
    PLUGIN_NAME = "MeiliSearch"
    PLUGIN_DESCRIPTION = "Syncs saleor data with MeiliSearch server."
    CONFIG_STRUCTURE = {
        "meilisearch_url": {
            "type": ConfigurationTypeField.STRING,
            "help_text": "The address of your MeiliSearch server",
            "label": "MeiliSearch URL",
        },
        "api_key": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": "Your MeiliSearch API key",
            "label": "API Key",
        },
    }
    DEFAULT_CONFIGURATION = [
        {"name": "meilisearch_url", "value": None},
        {"name": "api_key", "value": None},
    ]
    DEFAULT_ACTIVE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert to dict for easy access
        print("initx")
        self.config = {item["name"]: item["value"] for item in self.configuration}

    def _skip_plugin(self) -> bool:
        return not self.active or not self.config["meilisearch_url"]

    def product_created(self, product: "Product", previous_value: Any) -> Any:
        """Trigger when product is created.

        Overwrite this method if you need to trigger specific logic after a product is
        created.
        """
        print("product create")
        print(product)
        print(previous_value)
        # TODO: handle delete
        if not self._skip_plugin():
            if product.is_visible and product.is_available_for_purchase:
                docs = [serialize_product(product)]
                add_or_replace_documents.delay(
                    config=self.config, index="products", docs=docs
                )

    def product_updated(self, product: "Product", previous_value: Any) -> Any:
        """Trigger when product is updated.

        Overwrite this method if you need to trigger specific logic after a product is
        updated.
        """
        print("product update")
        print(product)
        print(previous_value)
        if not self._skip_plugin():
            if product.is_visible and product.is_available_for_purchase:
                docs = [serialize_product(product)]
                add_or_replace_documents.delay(
                    config=self.config, index="products", docs=docs
                )
