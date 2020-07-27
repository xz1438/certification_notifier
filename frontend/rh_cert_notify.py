#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Abnerson Malivert <amaliver@redhat.com>
# import libraries
import requests
import pandas as pd
import numpy as np
import smtplib
import re
import ssl
import ldap
import mysql.connector as mariadb
import datetime

from email.message import EmailMessage

"""
Email function for one recipient
recipient is one email
Password for redhat account will be standard input for the time being
Execute with email_recipient("example@company.com")
"""
def get_info(lists_len,dfs):
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

def get_owner_name(dfs):
    owner_info = dfs[0].iloc[1][1]
    return owner_info


def get_owner_info(owner):
    ldap_server = ldap.initialize('ldap://ldap.corp.redhat.com')
    ldap_server.simple_bind('dc=redhat,dc=com')
    search_result = ldap_server.search("dc=redhat,dc=com", ldap.SCOPE_SUBTREE, "cn=%s" % owner)
    ldap_server.set_option(ldap.OPT_REFERRALS, 0)
    result_type, result_data = ldap_server.result(search_result, 0)
    email = [ sub['mail'] for sub in result_data ]
    print(str(email))

def send_email(recipient):
    sender = "rhemailnotifier@gmail.com"
    msg = EmailMessage()

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Expiring certification"

    msg.set_content("Hello")

    s = smtplib.SMTP("smtp.gmail.com")
    s.starttls()
    s.login("rhemailnotifier@gmail.com", input("Sender password: "))
    s.sendmail(sender, recipient, msg.as_string())
    s.quit()


def insert_to_db (owner_name, cert_id, exam_info):

    # Dummy variables for email/manager
    people_manager = "John Doe"
    email_add = "sample@email.com"

    # Alias for cert names to be used as table names
    cert_alias = {
        'Red Hat Certified Specialist in Ansible Best Practices':"ansible_best_prac", 
        'Red Hat Certified Specialist in Ansible Automation':"ansible_auto",
        'Red Hat Certified Engineer':"RHCE",
        'Red Hat Certified System Administrator':"RHCSA"
        }

    # Need to manually enter in IP address of the MariaDB container
    host_ip = input("Enter MariaDB IP Address: ")

    try:
        conn = mariadb.connect(
        user="root",
        password="mypass",
        host=host_ip,
        # port=3307, #only need to specify if running from host machine
        database='certs')
        print ("DB connection success")

        cursor = conn.cursor()

        # Creating tables
        cursor.execute("create table personal_info (name varchar(255), cert_id varchar(255), people_manager varchar(255), email varchar(255), PRIMARY KEY(cert_id))")

        for cert in cert_alias:
            statement = "create table {cert_name} (name varchar(255), email varchar(255), cert_id varchar(255), tech varchar(255), date_received date, date_expire date, PRIMARY KEY(cert_id))".format(cert_name=cert_alias[cert])
            cursor.execute(statement)

        # Insert data into table
        personal_sql = "insert into personal_info (name, cert_id, people_manager, email) values (%s,%s,%s,%s)"
        personal_data = (owner_name, cert_id, people_manager, email_add)
        cursor.execute(personal_sql, personal_data)
        conn.commit()
        print ("Insert success into personal_info")

        for curr_cert in exam_info:
            table_name = cert_alias.get(curr_cert['cert'])
            sql = "insert into {exam} (name, email, cert_id, tech, date_received, date_expire) values (%s,%s,%s,%s,%s,%s)".format(exam=table_name)
            data = (owner_name, email_add, cert_id, curr_cert['tech'], curr_cert['date_received'], curr_cert['date_expire'])
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


def  main():
    # specify the url
    src_url = 'https://www.redhat.com/rhtapps/services/verify?certId=140-177-544'
    dfs = pd.read_html(src_url)
    owner = get_owner_name(dfs)
    # owner_info = dfs[0].iloc[1][0] + ' ' + dfs[0].iloc[1][1]
    # print(owner_info)
    cert_id = dfs[0].iloc[0][0].split()[0]
    list_len = len(dfs[1])
    result = get_info(list_len,dfs)
    #print(result)
    insert_to_db(owner, cert_id, result)

if __name__ == "__main__":
    main()
