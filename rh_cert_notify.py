#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Abnerson Malivert <amaliver@redhat.com>
# import libraries
import requests
import pandas as pd
import numpy as np
import re
import smtplib
import ssl

def get_info(lists_len):
    data_table = []
    x = 0
    while x < lists_len:
        list_data = dfs[1].iloc[x][0]
        split_data = re.split('Date:|Current|Until:|Technologies|Used:', str(list_data))
        exam_name = split_data[0]
        exam_date = split_data[1]
        exam_ex_date = split_data[3]
        tech_used = split_data[5]
        data_table.append([exam_name,tech_used,exam_date,exam_ex_date])
        x += 3
    return data_table 
    
# specify the url
src_url = 'https://www.redhat.com/rhtapps/services/verify?certId=140-177-544'

# parse the html using beautiful soup and store in variable `soup`

dfs = pd.read_html(src_url)
owner_info = dfs[0].iloc[1][0] + ' ' + dfs[0].iloc[1][1]
print(owner_info)
list_len = len(dfs[1]) - 3
result = get_info(list_len)
print(result)
