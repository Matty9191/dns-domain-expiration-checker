#!/usr/bin/env python
# Program: DNS Domain Expiration Checker
# Author: Matty < matty91 at gmail dot com >
# Current Version: 1.0
# Date: 07-20-2017
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

import time
import whois
import argparse
import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

DEBUG = 0
SMTP_TO = ""
SMTP_FROM = ""
SMTP_SERVER = ""


def debug(string_to_print):
    """
       Helper function to assist with printing debug messages.
    """
    if DEBUG:
        print(string_to_print)


def calculate_dns_expiration(domain, expire_days):
    """
       Check to see when a domain will expire
    """

    query_result = whois.query(domain)
    domain_expire = query_result.expiration_date - datetime.now()

    debug("Domain expire days %s, Expire warning days %s" % (domain_expire.days, expire_days))

    if domain_expire.days < expire_days:
        return domain_expire.days
    else:
        return 0


def check_expired(domainname, expiration_days, days_remaining):
    """
       Check to see if a domain has passed the expiration
       day threshold. If so send out notifications
    """
    if int(days_remaining) < int(expiration_days):
        domain_expire_notify(domainname, days_remaining)


def domain_expire_notify(domain, days):
    """
       Functions to call when a domain is about to expire. Adding support
       for Nagios, SNMP, etc. can be done by defining a new function and
       calling it here.
    """
    debug("Triggering notifications for the DNS domain %s" % domain)
    send_expire_email(domain, days)


def send_expire_email(domain, days):
    """
       Generate an e-mail to let someone know a domain is about to expire
    """
    debug("Generating an e-mail to %s for domain %s" % (SMTP_TO, domain))
    msg = MIMEMultipart()
    msg['From'] = SMTP_FROM
    msg['To'] = SMTP_TO
    msg['Subject'] = "The DNS Domain %s is set to expire in %d days" % (domain, days)

    body = "Time to renew %s" % domain
    msg.attach(MIMEText(body, 'plain'))

    smtp_connection = smtplib.SMTP(SMTP_SERVER)
    message = msg.as_string()
    smtp_connection.sendmail(SMTP_FROM, SMTP_TO, message)
    smtp_connection.quit()


def processcli():
    """
        parses the CLI arguments and returns a domain or 
        a file with a list of domains.
    """
    global SMTP_TO
    global SMTP_FROM
    global SMTP_SERVER
    global SMTP_PORT
    global DEBUG

    parser = argparse.ArgumentParser(description='DNS Statistics Processor')

    parser.add_argument('--domainfile', help="Path to file with list of domains and expiration intervals.")
    parser.add_argument('--domainname', help="Domain to check expiration on.")
    parser.add_argument('--debug',action="store_true", help="Enable debugging output.")
    parser.add_argument('--expiredays', default=90, help="Expiration threshold to check against.")
    parser.add_argument('--sleeptime', default=5, help="Time to sleep between whois queries.")
    parser.add_argument('--smtpserver', default="localhost", help="SMTP server to use.")
    parser.add_argument('--smtpport', default=25, help="SMTP port to connect to.")
    parser.add_argument('--smtpto', default="root", help="SMTP To: address.")
    parser.add_argument('--smtpfrom', default="root", help="SMTP From: address.")
    args = parser.parse_args()

    # TODO: Need to research ways to hold the SMTP configs w/o globals.
    SMTP_TO = args.smtpto
    SMTP_FROM = args.smtpfrom
    SMTP_PORT = args.smtpport
    SMTP_SERVER = args.smtpserver
    DEBUG = args.debug

    return args.domainfile, args.domainname, args.expiredays, args.sleeptime


def main():
   """
       Main loop
   """
   days_remaining = 0
   domainfile, domainname, expire_days, sleeptime =  processcli()

   if domainfile:
       with open(domainfile, "r") as domains_to_process:
           for line in domains_to_process:
                domainname, expiration_days = line.split()
                debug("Checking domain %s" % domainname)
                days_remaining = calculate_dns_expiration(domainname, expiration_days)
                check_expired(domainname, expiration_days, days_remaining)
                time.sleep(sleeptime)
   elif domainname:
       debug("Checking domain %s" % domainname)
       days_remaining = calculate_dns_expiration(domainname, expire_days)
       check_expired(domainname, expire_days, days_remaining)
       time.sleep(sleeptime)


if __name__ == "__main__":
    main()
