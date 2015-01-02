#-------------------------------------------------------------------------------
# Name:        Weld Programming Exercise
# Purpose:     Email Data analysis for Amazon orders
#
# Author:      Usbaldo Balderas
#
# Created:     01/01/2015
# Copyright:   (c) Usbaldo Balderas 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import imaplib
import email
import datetime
import time

'''Generating a uid list given a list of sender addresses and since date'''
def uids_from_sender_and_date(date,sender_list):
    uids = []
    for addr in sender_list:
        content_str = '(SENTSINCE {date} HEADER From "'+addr+'")'
        result, data = mail.uid('search', None, content_str.format(date=date))
        uids+=data[0].split()

    return uids

'''Extracting dates from a uid list'''
def email_dates(uid_list):
    purchase_dates = []
    purchase_months = []
    for uid in uid_list:

        result, data = mail.uid('fetch', uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        purchase_date = time.strptime(email_message['Date'][:-6],'%a, %d %b %Y %H:%M:%S')
        purchase_dates.append([purchase_date.tm_mon, purchase_date.tm_mday, purchase_date.tm_year])
        purchase_months.append(purchase_date.tm_mon)

    return purchase_dates, purchase_months



'''Gmail login and connection to inbox'''
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('usbaldo.balderas@gmail.com', 'notthatuser')
mail.select("inbox") # connect to inbox.


'''Time restriction for search'''
years_limit = 2
date = (datetime.date.today() - datetime.timedelta(365*years_limit)).strftime("%d-%b-%Y")

'''Search restricted to incoming email from order confirmations from Amazon'''
amazon_addresses = ["auto-confirm@amazon.com", "digital-no-reply@amazon.com" ]
amazon_uids = uids_from_sender_and_date(date,amazon_addresses)
p_dates, p_months = email_dates(amazon_uids)

'''Analysis of Purchases by month'''
monthly_purchases = {m:p_months.count(m) for m in p_months}
monthly_purchases_probability = {m:100*float(monthly_purchases[m])/len(p_months) for m in monthly_purchases}

print monthly_purchases_probability






