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
import mysql.connector as mariadb
import datetime

def get_info(lists_len):
    data_table = []
    x = 0
    while x < lists_len:
        list_data = dfs[1].iloc[x][0]
        split_data = re.split('Date:|Current|Until:|Technologies|Used:', str(list_data))
        exam_name = split_data[0].strip()
        exam_date = split_data[1].strip()
        exam_date_obj = datetime.datetime.strptime(exam_date, '%b %d, %Y')
        exam_ex_date = split_data[3].strip()
        exam_ex_date_obj = datetime.datetime.strptime(exam_date, '%b %d, %Y')
        tech_used = split_data[5].strip()
        data_table.append({"cert": exam_name,"tech": tech_used, "date_received": exam_date_obj.date(), "date_expire": exam_ex_date_obj.date()})
        x += 3
    return data_table 
    
# specify the url
src_url = 'https://www.redhat.com/rhtapps/services/verify?certId=140-177-544'

# parse the html using beautiful soup and store in variable `soup`

dfs = pd.read_html(src_url)
owner_info = dfs[0].iloc[1][0] + ' ' + dfs[0].iloc[1][1]
owner_name = dfs[0].iloc[1][1]
cert_id = dfs[0].iloc[0][0].split()[0]
print (owner_name + ' ' + cert_id)
list_len = len(dfs[1])
result = get_info(list_len)
print(result)

cert_alias = {
    'Red Hat Certified Specialist in Ansible Best Practices':"ansible_best_prac", 
    'Red Hat Certified Specialist in Ansible Automation':"ansible_auto",
    'Red Hat Certified Engineer':"RHCE",
    'Red Hat Certified System Administrator':"RHCSA"
    }

try:
   conn = mariadb.connect(
      user="root",
      password="mypass",
      host="0.0.0.0",
      port=3308,
      database='certs')
   print ("DB connection success")

   cursor = conn.cursor()

   # Creating tables
   cursor.execute("create table RHCE (name varchar(255), email varchar(255), cert_id varchar(255), tech varchar(255), date_received date, date_expire date, PRIMARY KEY(name))")
   cursor.execute("create table RHCSA (name varchar(255), email varchar(255), cert_id varchar(255), tech varchar(255), date_received date, date_expire date, PRIMARY KEY(name))")
   cursor.execute("create table ansible_auto (name varchar(255), email varchar(255), cert_id varchar(255), tech varchar(255), date_received date, date_expire date, PRIMARY KEY(name))")
   cursor.execute("create table ansible_best_prac (name varchar(255), email varchar(255), cert_id varchar(255), tech varchar(255), date_received date, date_expire date, PRIMARY KEY(name))")

   # Insert data into table
   for curr_cert in result:
       table_name = cert_alias.get(curr_cert['cert'])
       sql = "insert into {exam} (name, cert_id, tech, date_received, date_expire) values (%s,%s,%s,%s,%s)".format(exam=table_name)
       data = (owner_name, cert_id, curr_cert['tech'], curr_cert['date_received'], curr_cert['date_expire'])
       cursor.execute(sql,data)
       conn.commit()
       print ("Insert success into " + table_name)


except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")

finally:
   if (conn.is_connected()):
      cursor.close()
      conn.close()
      print("DB connection closed")