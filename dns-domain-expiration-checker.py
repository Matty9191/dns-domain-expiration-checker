#!/usr/bin/env python
# Program: DNS Domain Expiration Checker
# Author: Matty < matty91 at gmail dot com >
# Current Version: 1.2
# Date: 07-24-2017
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

import sys
import time
import whois
import argparse
import smtplib
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

DEBUG = 0

def debug(string_to_print):
    """
       Helper function to assist with printing debug messages.
    """
    if DEBUG:
        print(string_to_print)


def print_heading():
    """
       Print a formatted heading when called interactively
    """
    print("%-25s  %-30s  %-20s  %-4s" % ("Domain Name", "Registrar", "Expiration Date", "Days Left"))


def print_domain(domain, registrar, expiration_date, days_remaining):
    """
       Pretty print the domain information on stdout
    """
    print("%-25s  %-30s  %-20s  %-4s" % (domain, registrar, expiration_date, days_remaining))


def send_whois_query(domain):
    """
       Issue a WHOIS query for the domain passed as an argument. return
       the expiration date and registrar
    """
    debug("Sending a WHOIS query for the domain %s" % domain)
    try:
        query_result = whois.query(domain)
    except:
        print("Unable to retrieve WHOIS data for domain %s" % domain)
        sys.exit(1)

    return query_result.expiration_date, query_result.registrar


def calculate_expiration_days(expire_days, expiration_date):
    """
       Check to see when a domain will expire
    """
    try:
        domain_expire = expiration_date - datetime.now()
    except:
        print("The registrar date formats may have changed.")
        print("Please send a copy of your WHOIS data to the program author")
        sys.exit(1)

    debug("Domain expire days %s, Expire warning days %s" % (domain_expire.days, expire_days))

    if domain_expire.days < expire_days:
        return domain_expire.days
    else:
        return 0


def check_expired(expiration_days, days_remaining):
    """
       Check to see if a domain has passed the expiration
       day threshold. If so send out notifications
    """
    if int(days_remaining) < int(expiration_days):
        return days_remaining
    else:
        return 0


def domain_expire_notify(domain, config_options, days):
    """
       Functions to call when a domain is about to expire. Adding support
       for Nagios, SNMP, etc. can be done by defining a new function and
       calling it here.
    """
    debug("Triggering notifications for the DNS domain %s" % domain)

    # Send outbound e-mail if a rcpt is passed in
    if config_options["email"]:
        send_expire_email(domain, days)


def send_expire_email(domain, days, config_options):
    """
       Generate an e-mail to let someone know a domain is about to expire
    """
    debug("Generating an e-mail to %s for domain %s" % (config_options["smtpto"], domain))
    msg = MIMEMultipart()
    msg['From'] = config_options["smtpfrom"]
    msg['To'] = config_options["smtpto"]
    msg['Subject'] = "The DNS Domain %s is set to expire in %d days" % (domain, days)

    body = "Time to renew %s" % domain
    msg.attach(MIMEText(body, 'plain'))

    smtp_connection = smtplib.SMTP(config_options["smtpserver"],config_options["smtpport"])
    message = msg.as_string()
    smtp_connection.sendmail(config_options["smtpfrom"], config_options["smtpto"], message)
    smtp_connection.quit()


def processcli():
    """
        parses the CLI arguments and returns a domain or 
        a file with a list of domains.
    """
    parser = argparse.ArgumentParser(description='DNS Statistics Processor')

    parser.add_argument('--domainfile', help="Path to file with list of domains and expiration intervals.")
    parser.add_argument('--domainname', help="Domain to check expiration on.")
    parser.add_argument('--email', action="store_true", help="Enable debugging output.")
    parser.add_argument('--interactive',action="store_true", help="Enable debugging output.")
    parser.add_argument('--expiredays', default=90, help="Expiration threshold to check against.")
    parser.add_argument('--sleeptime', default=5, help="Time to sleep between whois queries.")
    parser.add_argument('--smtpserver', default="localhost", help="SMTP server to use.")
    parser.add_argument('--smtpport', default=25, help="SMTP port to connect to.")
    parser.add_argument('--smtpto', default="root", help="SMTP To: address.")
    parser.add_argument('--smtpfrom', default="root", help="SMTP From: address.")

    # Return a dict() with all of the arguments passed in
    return(vars(parser.parse_args()))


def main():
   """
       Main loop
   """
   days_remaining = 0
   conf_options = processcli()

   if conf_options["interactive"]:
       print_heading()
   
   if conf_options["domainfile"]:
       with open(conf_options["domainfile"], "r") as domains_to_process:
           for line in domains_to_process:
                domainname, expiration_days = line.split()
                expiration_date, registrar = send_whois_query(domainname)
                days_remaining = calculate_expiration_days(expiration_days, expiration_date)

                if check_expired(expiration_days, days_remaining):
                    domain_expire_notify(domainname, conf_options, days_remaining)

                if conf_options["interactive"]:
                    print_domain(domainname, registrar, expiration_date, days_remaining)

                # Need to wait between queries to avoid triggering DOS measures like so:
                # Your IP has been restricted due to excessive access, please wait a bit
                time.sleep(conf_options["sleeptime"])

   elif conf_options["domainname"]:
       expiration_date, registrar = send_whois_query(conf_options["domainname"])
       days_remaining = calculate_expiration_days(conf_options["expiredays"], expiration_date)

       if check_expired(conf_options["expiredays"], days_remaining):
           domain_expire_notify(conf_options["domainname"], conf_options, days_remaining)

       if conf_options["interactive"]:
           print_domain(conf_options["domainname"], registrar, expiration_date, days_remaining)

       # Need to wait between queries to avoid triggering DOS measures like so:
       # Your IP has been restricted due to excessive access, please wait a bit
       time.sleep(conf_options["sleeptime"])


if __name__ == "__main__":
    main()
