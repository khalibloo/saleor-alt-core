from setuptools import setup

setup(
    entry_points={
        "saleor.plugins": ["meilisearch = meilisearch.plugin:MeiliSearchPlugin"]
    }
)
