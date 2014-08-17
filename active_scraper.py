__author__ = 'sutedja'

import csv

from datetime import datetime
from urllib2 import urlopen
from bs4 import BeautifulSoup

from util import get_text_if_exists, clean_string

base_url = 'http://www.active.com/running?sort=date_asc'

soup = BeautifulSoup(urlopen(base_url).read())
event_list = []

with open('/home/sutedja/personal/races/active_race_list.csv', "w") as f:
    headers = ("Date", "Day", "Event Name", "url", "Types", "Prices", "Location",
              # "Awards",
               "Notes")
    output = csv.DictWriter(f, headers)
    output.writeheader()

    events = soup.find("section", "section activities-block refined-search-container").find("div", {"id": "lpf-tabs2-a"}).find_all("article")
    for event in events:
        event_name = get_text_if_exists(event, "h5", {"class": "title"})
        event_date = event.find("span", {"itemprop": "startDate"})["content"].split("T")[0]
        lat, long = [float(x) for x in event["data-geo-point"].split(',')]
        detail_url = 'http://www.active.com' + event.find("a", "ie-article-link" )["href"]
        types = get_text_if_exists(event, "h6", {"class":"secondary-text desc-info pull-left"})
        detail_soup = BeautifulSoup(urlopen(detail_url).read())
        event_day = get_text_if_exists(detail_soup.find("div", "visible-desktop"), "h5").split(",")[0]
        address_name = get_text_if_exists(detail_soup, "span", {"itemprop": "name"})
        address = clean_string(get_text_if_exists(detail_soup, "span", {"itemprop": "address"}), utf8=True)
        notes = clean_string(get_text_if_exists(detail_soup, "div", {"itemprop": "description"}), utf8=True)
        prices = []
        has_prices = detail_soup.find("div", "price-grid")
        if has_prices:
            name_prices = has_prices.find_all("div", "row price-row")
            for name_price in name_prices:
                event_type = get_text_if_exists(name_price, "h5", {"itemprop": "name"})
                price = get_text_if_exists(name_price, "h5", {"itemprop": "Price"})
                prices.append((event_type, price))
        event_dict = {"Date": None,
                       "Day": event_day,
                       "Event Name": event_name,
                       "url": detail_url,
                       "Types": types,
                       "Location": address,
                       "Prices": prices,
                       "Notes": notes}
        print event_dict
        event_list.append(event_dict)
    output.writerows(event_list)
    print len(event_list)