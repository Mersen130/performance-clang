from html.parser import HTMLParser
import requests
import os
import hashlib


remote = "http://104.154.54.203"

class MyHTMLParser(HTMLParser):
    count = 0
    tag = True
    data = None

    def handle_starttag(self, tag, attrs):
        if tag == "a" and attrs and "graph" in attrs[0][1] and attrs[0][1][0] == '/':
            self.tag = True
            
#             if self.count >= 5:
#                 exit(0)
            self.count += 1
            print("Starting {}: {}".format(self.count, "MODE=text\nURL={}".format(remote + attrs[0][1])))
            

            with open(".env", "w") as f:
                f.write("MODE=text\nURL={}".format(remote + attrs[0][1]))
            filename = str(int(hashlib.sha256(attrs[0][1].encode('utf-8')).hexdigest()[:16], 16)-2**63)

            
    def handle_endtag(self, tag):
        if self.tag:
            os.system("python3 fetch_1benchmark.py > {}".format("results/" + self.data))
            print("{} Done".format(self.count))
        self.tag = False
        
    def handle_data(self, data):
        if self.tag:
            self.data = data.split("/")[-1]



p = MyHTMLParser()
response = requests.request("GET", "http://104.154.54.203/db_default/v4/nts/147402", data={})

p.feed(response.text)
p.close()

 
