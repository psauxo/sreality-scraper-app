import scrapy


class PageItem(scrapy.Item):
    """
    The PageItem is a class that represents a scraped item from the sreality.cz website.
    The item has two fields:
    - title: title of the listing (e.g. "2+kk, 50m²")
    - image_url: url of the listing's image
    """

    title = scrapy.Field()
    image_url = scrapy.Field()
