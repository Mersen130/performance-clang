from html.parser import HTMLParser
import requests
import os
import hashlib


remote = "http://104.154.54.203"

class MyHTMLParser(HTMLParser):
    count = 0
    tag = False
    data = None
    url = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a" and attrs and "graph" in attrs[0][1] and attrs[0][1][0] == '/':
            self.tag = True
            
#             if self.count >= 5:
#                 exit(0)
            self.count += 1
#             print("Starting {}: {}".format(self.count, "MODE=text\nURL={}".format(remote + attrs[0][1])))

            with open(".env", "w") as f:
                self.url = remote + attrs[0][1]
                f.write("MODE=text\nURL={}".format(self.url))
            filename = str(int(hashlib.sha256(attrs[0][1].encode('utf-8')).hexdigest()[:16], 16)-2**63)

            
    def handle_endtag(self, tag):
        if self.tag:
            if (os.path.exists("results/" + self.data) and os.path.getsize("results/" + self.data) == 0) or not os.path.exists("results/" + self.data):
#             print("self.data: " + self.data)
#             print(open("results/" + self.data).read())
#                 print((os.path.exists("results/" + self.data) and os.path.getsize("results/" + self.data) == 0), not os.path.exists("results/" + self.data))
#             os.system("python3 fetch_1benchmark.py > {}".format("results/" + self.data))
                print(self.url, self.data)
        self.tag = False
        
    def handle_data(self, data):
        if self.tag:
            self.data = data.split("/")[-1].strip()



p = MyHTMLParser()
response = requests.request("GET", "http://104.154.54.203/db_default/v4/nts/147402", data={})

p.feed(response.text)
p.close()

 
