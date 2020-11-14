from django.core.exceptions import ObjectDoesNotExist

from saleor.product.models import Product


def serialize_product(product: Product):
    # base document
    doc = {
        "id": product.id,
        "name": product.name,
        "description": product.seo_description,
        "category": product.category.name,
        "slug": product.slug,
    }

    for t in product.translations.all():
        doc["name_" + t.language_code] = t.name
        doc["description_" + t.language_code] = t.description

    for attr in product.attributes.all():
        # add field for attribute
        doc["attr::" + attr.attribute.slug] = attr.values.first().name
        for t in attr.attribute.translations.all():
            # only add translation for attribute if it has a corresponding attr value translation
            try:
                value_trans = attr.values.first().translations.get(
                    language_code=t.language_code
                )
                doc[
                    "attr_" + t.language_code + "::" + attr.attribute.slug
                ] = value_trans.name
            except ObjectDoesNotExist:
                pass

    return doc
