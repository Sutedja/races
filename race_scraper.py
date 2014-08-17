import csv
import re

from datetime import datetime
from urllib2 import urlopen

from bs4 import BeautifulSoup

base_url = 'http://www.raceplace.com/crunsd.shtml'

soup = BeautifulSoup(urlopen(base_url).read())
event_list = []

def get_event_date(date_string):
    return [int(x.lstrip("0")) for x in date_string.encode("utf-8").replace("\xc2\xa0", "").strip().split("/")]

def get_event_time(time_string):
    h, m_am_pm = time_string.lower().split(":")
    m = re.findall('\d+', m_am_pm)[0]
    am_pm = m_am_pm.strip(m).strip()
    h, m = int(h), int(m)
    if am_pm == 'pm':
        h += 12
    return h, m

def convert_time(y, m, d, hour=None, minute=None):
    y, m, d = int(y), int(m), int(d)
    time = datetime(y, m, d)
    if hour and minute:
        time = datetime(y, m, d, hour=hour, minute=minute)
    return time

def get_date_day_time_dict(date_day_time_string):
    parts = date_day_time_string.split("*$*")
    date_list = filter(lambda x: "/" in x, parts)
    time_list = filter(lambda x: ":" in x, parts)
    day_list = filter(lambda x: "day" in x, parts)
    date = ""
    if date_list:
        date =  get_event_date(date_list[0])
    return {"date": date,
            "time": time_list[0] if time_list else "",
            "day": day_list[0] if day_list else ""}

def get_text_if_exists(soup_part, tag, class_attr=None):
    element = soup_part.find(tag, class_attr) if class_attr else soup_part.find(tag)
    return element.get_text().strip().encode('utf-8') if element else ''

with open('/home/sutedja/personal/races/race_list.csv', "w") as f:
    headers = ("Date", "Day", "Event Name", "url", "Types", "Location",
              # "Awards",
               "Notes")
    output = csv.DictWriter(f, headers)
    output.writeheader()

    table = soup.find("table", "calendar")
    events = table.find_all("tr", {"class": ["ob", "e", "eb"]})
    for event in events:
        date_day_time = event.find("td", "date").get_text("*$*").encode('utf-8').replace("\xc2\xa0", "*$*")
        date_day_time_dict = get_date_day_time_dict(date_day_time)
        [m, d, y], event_day, event_time = date_day_time_dict.get("date"), date_day_time_dict.get("day"), date_day_time_dict.get("time")
        hour, minute = None, None
        if event_time:
            hour, minute = get_event_time(event_time)
        event_datetime = convert_time(y, m, d, hour=hour, minute=minute)
        event_name = get_text_if_exists(event, "td", "name")
        type_pattern = re.compile('((\d+)\s?(miles?|mi|k))|((half|1/2)?\s?marathon)', re.IGNORECASE)
        event_types = map(lambda y: y[0].strip(),[sorted(list(x), key=len, reverse=True) for x in type_pattern.findall(event_name)])
        url = event.find("td", "misc").find("a").get_text() if event.find("td", "misc") and event.find("td", "misc").find("a") else ''
        location = get_text_if_exists(event, "td", "location")
        notes = get_text_if_exists(event, "td", "misc")
        event_dict = {"Date": event_datetime,
                           "Day": event_day,
                           "Event Name": event_name,
                           "url": url.strip(),
                           "Types": event_types,
                           "Location": location,
                           #"Awards": None,
                           "Notes": notes}
        print event_dict
        event_list.append(event_dict)
    output.writerows(event_list)
    print len(event_list)