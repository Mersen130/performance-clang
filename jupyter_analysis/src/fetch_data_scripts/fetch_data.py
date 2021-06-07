#!/usr/bin/env python
# coding: utf-8

# In[46]:


import hashlib
import re
import requests
import json
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from html.parser import HTMLParser
from os import path
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import csv
import os
from dotenv import load_dotenv


# In[48]:


load_dotenv()
MODE = os.getenv("MODE")  # no graphical output iff MODE=text
url = os.getenv("MODE")


# In[55]:


# update me

filename = "../../data/" + str(int(hashlib.sha256(url.encode('utf-8')).hexdigest()[:16],
                  16)-2**63)
# print("cached filename:", filename)

if not path.exists(filename):
    payload = {}

    response = requests.request("GET", url, data=payload)

    with open(filename, "w") as f:
        f.write(response.text)


# In[51]:


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



# In[56]:


def filter_by_date(points):
    one_month = date.today() - relativedelta(days=7)
    one_month = datetime.datetime(one_month.year, one_month.month, one_month.day)
    return [p for p in points if p[2] > one_month]


# In[57]:


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
            
            # convert string dates to manipulatable datetimes
            for p in points:
                p[2]["date"] = datetime.datetime.strptime(p[2]["date"], '%Y-%m-%d %H:%M:%S')
                p.insert(2, p[2]["date"])
                del p[3]["date"]
            
            with open(filename + ".csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([["sequence", "execution time", "date", "metadata"]] + points)

            points_df = pd.DataFrame(points,columns=["sequence", "execution time", "date", "metadata"])  # points_df is a dataframe
            
            points_1_week = filter_by_date(points)
#             print(len(points))
            if MODE != "text":
        
                display(points_df)
            
                print(points_1_week[0])
                print(points_1_week[1])
                print(points_1_week[2])
                print("...", len(points_1_week), "points found ...")
            break


# In[58]:


def plot_seq():
    # points sort by sequence number
    fig = plt.figure(figsize=(20,12))
    xs = [p[0] for p in points_1_week]
    ys = [p[1] for p in points_1_week]
    
    max_diff = float("-inf")
    last = None
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > max_diff:
                max_diff = abs(last - ys[i])

    last = None

    plt.plot(xs, ys)
    plt.xlabel('sequence')
    plt.ylabel('execution time')
    plt.grid(True)
    plt.show()

    print("Summary:")
    print("\tpairs of consecutive points that differs over 80% of the maximum difference:")
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > 0.8 * max_diff:
                print("\t  {}, {}".format(xs[i - 1], xs[i]))

if MODE != "text":
    plot_seq()


# In[61]:


# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
 
    while low <= high:
 
        mid = (high + low) // 2
 
        # If x is greater, ignore left half
        if arr[mid][2] < x:
            low = mid + 1
 
        # If x is smaller, ignore right half
        elif arr[mid][2] > x:
            high = mid - 1
 
        # means x is present at mid
        else:
            return mid
 
    # If we reach here, then the element was not present
    return -1

def plot_date():
    # points sort by dates
    points_1_week.sort(key=lambda p: p[2])
    dates = [p[2] for p in points_1_week]
    ys = [p[1] for p in points_1_week]

    max_diff = float("-inf")
    last = None
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > max_diff:
                max_diff = abs(last - ys[i])

    if MODE != "text":
        fig = plt.figure(figsize=(20,12))
        plt.plot(dates, ys)
        plt.xlabel('date')
        plt.ylabel('execution time')
        plt.grid(True)
        plt.show()

        last = None
        print("Summary:")
        print("\tpairs of consecutive points that differs over 80% of the maximum difference:")
        for i in range(len(ys)):
            if not last:
                last = ys[i]
            else:
                if abs(last - ys[i]) > 0.8 * max_diff:
                    print("\t  {}, {}".format(dates[i - 1], dates[i]))
    else:
            
        last = None
        for i in range(len(ys)):
            if not last:
                last = ys[i]
            else:
                if abs(last - ys[i]) > 0.8 * max_diff:
                    print("{}, {}".format(points_1_week[binary_search(points_1_week, dates[i - 1])][3]["label"], points_1_week[binary_search(points_1_week, dates[i])][3]["label"]))
    
plot_date()


# In[62]:


def plot_ma_seq():
    ys = points_df["execution time"].groupby(np.arange(len(points_df))//100).mean()
    xs = [100*i for i in range(len(ys))]
    plt.style.use('seaborn-dark')
    plt.style.use("tableau-colorblind10")

    fig = plt.figure(figsize=(20,12))
    ax1 = plt.plot(xs, ys)
    ax1 = plt.title("Execution Time Moving Average", fontsize=22)
    ax1 = plt.xlabel("Sequence", fontsize=18)
    ax1 = plt.ylabel("Moving Average", fontsize=18)
    # ax1 = plt.legend(["100 day SMA"],prop={"size":20}, loc="upper left")
    plt.grid(True)
    plt.show()

    max_diff = float("-inf")
    last = None
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > max_diff:
                max_diff = abs(last - ys[i])

    last = None
    print("Summary:")
    print("\tpairs of consecutive points that differs over 80% of the maximum difference:")
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > 0.8 * max_diff:
                print("\t  {}, {}".format(xs[i - 1], xs[i]))
                
if MODE != "text":
    plot_ma_seq()


# In[63]:


def plot_ma_date():
    points_by_time_df = points_df.sort_values(by=['date'])

    ys = points_df["execution time"].groupby(np.arange(len(points_df))//100).mean()
    xs = points_by_time_df["date"].iloc[::100]

    plt.style.use('seaborn-dark')
    plt.style.use("tableau-colorblind10")

    fig = plt.figure(figsize=(20,12))
    ax1 = plt.plot(xs, ys)
    ax1 = plt.title("Execution Time Moving Average", fontsize=22)
    ax1 = plt.xlabel("Sequence", fontsize=18)
    ax1 = plt.ylabel("Moving Average", fontsize=18)
    # ax1 = plt.legend(["100 day SMA"],prop={"size":20}, loc="upper left")
    plt.grid(True)
    plt.show()

    max_diff = float("-inf")
    last = None
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > max_diff:
                max_diff = abs(last - ys[i])

    last = None
    print("Summary:")
    print("\tpairs of consecutive points that differs over 80% of the maximum difference:")
    for i in range(len(ys)):
        if not last:
            last = ys[i]
        else:
            if abs(last - ys[i]) > 0.8 * max_diff:
                print("\t  {}, {}".format(xs.iloc[i - 1], xs.iloc[i]))
                
if MODE != "text":
    plot_ma_date()

