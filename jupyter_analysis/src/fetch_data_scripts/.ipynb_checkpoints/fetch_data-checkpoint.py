import hashlib
import re
import requests
import json
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from html.parser import HTMLParser
from os import path

# update me
url = "http://104.154.54.203/db_default/v4/nts/graph?highlight_run=145241&plot.1605785=1364.1605785.3"
filename = str(int(hashlib.sha256(url.encode('utf-8')).hexdigest()[:16],
                  16)-2**63) + ".txt"
print("cached filename:", filename)

if not path.exists(filename):
    payload = {}

    response = requests.request("GET", url, data=payload)

    with open(filename, "w") as f:
        f.write(response.text)


class MyHTMLParser(HTMLParser):
    js_encountered = False

    def handle_starttag(self, tag, attrs):
        if tag != "script" or attrs != [('type', 'text/javascript')]:
            return
        self.js_encountered = True
        print("Encountered a start tag:", tag, attrs)

    def handle_endtag(self, tag):
        if not self.js_encountered:
            return
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if not self.js_encountered:
            return
        self.js_encountered = False
        print("Encountered some data  :", data)
        print(data)
        print(data.index("graph_plots"))


def filter_by_date(points):
    one_month = date.today() - relativedelta(months=1)
    one_month = datetime.datetime(one_month.year, one_month.month, one_month.day)
    return [p for p in points if datetime.datetime.strptime(p[2]["date"], '%Y-%m-%d %H:%M:%S') > one_month]


with open(filename, "r") as f:
    # parser = MyHTMLParser()
    # parser.feed(f.read())
    for line in f:
        if "overview_plots" in line:
            line = line.strip()
            # print(line)
            values = re.findall(r'var.*?=\s*(.*?);', line, re.DOTALL |
                                re.MULTILINE)
            # print((values[0][:10]))
            points = json.loads(values[0])
            points = points[0]["data"]  # a list of data points

            points = filter_by_date(points)
            print(points[0])
            print(points[1])
            print(points[2])
            print("...", len(points), "points found ...")
            break
