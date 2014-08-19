# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RacesItem(Item):
    event_date = Field()
    event_day = Field()
    event_name = Field()
    url = Field()
    types = Field()
    prices = Field()
    location = Field()
    notes = Field()

N