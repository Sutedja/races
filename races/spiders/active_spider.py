from scrapy.spider import Spider
from scrapy.selector import Selector

class ActiveSpider(Spider):
    name = "active"
    allowed_domains = ["active.com/running"]
    start_urls = [
        "http://www.active.com/running/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        sel = Selector(response)
        events = sel.xpath('//div[@id="lpf-tabs2-a"]//article[@class="ie-activity-list "]')
        for event in events:
            event.extract()
        with open(filename, 'wb') as f:
            f.write(response.body)