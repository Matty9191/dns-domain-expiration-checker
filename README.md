# Checking DNS Domain Expiration

If you are here you may have had a domain expire and dealt with the annoyances that go with reclaiming it. It's no fun is it? To prevent yourself from dealing with this again you can install and run dns-domain-expiration-checker.py to monitor your domains. The script is easy to install and will send you an e-mail if your domain is set to expire in the near future. You can also use the script to view the registrars and expiration dates for your domains. Now to some examples.

To interactively view the expiration dates and registrars for a list of domains run the script with the "--interactive
" option:
<pre>
$ dns-domain-expiration-checker.py --interactive --domainfile domains
Domain Name                Registrar                       Expiration Date       Days Left
prefetch.net               DNC HOLDINGS, INC.              2020-06-23 00:00:00   1064
spotch.com                 GANDI SAS                       2017-12-03 00:00:00   131 
google.com                 MARKMONITOR INC.                2020-09-14 00:00:00   1147
</pre>

To generate an e-mail when a domain is about to expire you can pass a domain and threshold to the script:

<pre>
$ dns-domain-expiration-checker.py --domainname prefetch.net --email --expiredays 90
</pre>

This will generate an e-mail if the domain prefetch.net is set to expire in the next 90-days. You can also add several domains and expiration intervals to a file and pass that as an argument:

<pre>
$ cat domains
spotch.com 60
yahoo.com 60
prefetch.net 2000
google.com 80

$ dns-domain-expiration-checker.py --domainfile domains --email --smtpserver smtp.mydomain --smtpto "biff" --smtpfrom "Root"
</pre>

# Installation

The dns-domain-expiration-checker.py script relies on the dateutil PiPY pacakge to normalize dates. Here are the steps to get this script working:

1. Create a virtualenv to run dns-domain-expiration-checker in:
<pre>
$ mkproject dns-domain-expiration-checker
</pre>
2. Surf over to that new environment:
<pre>
$ workon dns-domain-expiration-checker
</pre>
3. Pull down dateutils with pip:
<pre>
$ pip install dateutil
</pre>
4. Clone this repo:
<pre>
$ git clone https://github.com/Matty9191/dns-domain-expiration-checker.git
</pre>
5. Run the script against the domains you want to check (this assume you are in the root of your virtualenv):
<pre>
$ dns-domain-expiration-checker/ns-domain-expiration-checker.py ....
</pre>
6. Automate the domain checking process.




