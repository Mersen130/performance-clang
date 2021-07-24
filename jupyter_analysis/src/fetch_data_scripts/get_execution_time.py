from html.parser import HTMLParser
import requests
import os
import hashlib
import re
import json
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from html.parser import HTMLParser
from os import path
import os

remote = "http://104.154.54.203"
MODE = "text"




def get_points(url, benchmark_name):
    filename = str(int(hashlib.sha256(url.encode('utf-8')).hexdigest()[:16],
                  16)-2**63)

    # fetch lnt data
    if not path.exists("../../data/" + filename):
        payload = {}

        response = requests.request("GET", url, data=payload)

        with open("../../data/" + filename, "w") as f:
            f.write(response.text)

    with open("../../data/" + filename, "r") as f:
        # parser = MyHTMLParser()
        # parser.feed(f.read())
        for line in f:
            if "overview_plots" in line:
                line = line.strip()
    #             print(line)
                values = re.findall(r'var.*?=\s*(.*?);', line, re.DOTALL |
                                    re.MULTILINE)
    #             print((values[0][:10]))
                points = json.loads(values[0])
                points = points[0]["data"]  # a list of data points
            
                return points


class MyHTMLParser(HTMLParser):
    count = 0
    tag = False
    data = None
    url = ""

    def handle_starttag(self, tag, attrs):
#         print(tag)
        if tag == "a" and attrs and "graph" in attrs[0][1] and attrs[0][1][0] == '/':
            self.tag = True
            
#             if self.count >= 5:
#                 exit(0)
            self.count += 1
#             print("Starting {}: {}".format(self.count, "MODE=text\nURL={}".format(remote + attrs[0][1])))

            self.url = remote + attrs[0][1]
            filename = str(int(hashlib.sha256(attrs[0][1].encode('utf-8')).hexdigest()[:16], 16)-2**63)

            
    def handle_endtag(self, tag):
#         print(tag)
#         print(self.url, self.data)
        if self.tag:
            points = get_points(self.url, self.data)
            with open("results/" + self.data) as f:
                com1, com2 = f.readline().strip().split(" ")
                t1 = None
                t2 = None
                for p in points:
                    if com1 == p[2]['label']:
                        t1 = p[1]
                    elif com2 == p[2]['label']:
                        t2 = p[1]
                with open("results/execution_time/" + self.data, "w") as f2:
                    f2.write("{} {}\n".format(t1, t2))
                    f2.write(str(((t1-t2)/t1)*100) + "%")
            
        self.tag = False
        
        
    def handle_data(self, data):
#         print(data)
        if self.tag:
            self.data = data.split("/")[-1].strip()



p = MyHTMLParser()
if not path.exists("../../data/nts147402"):
    response = requests.request("GET", "http://104.154.54.203/db_default/v4/nts/147402", data={})
    with open("../../data/nts147402", "w") as f:
        f.write(response.text)

    p.feed(response.text)
    p.close()
else:
    with open("../../data/nts147402") as f:
        res = f.read()
        p.feed(res)
