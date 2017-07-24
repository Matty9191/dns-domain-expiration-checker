# Checking DNS Domain Expiration

If you are here you may have had a domain expire and dealt with the annoyances that go with reclaiming it. It's no fun is it? To prevent yourself from dealing with this again you can install and run dns-domain-expiration-checker to monitor your domains. The script is easy to install and will send you an e-mail if your domain is set to expire in the near future. You can also use the scriupt to view the registrars and expiration dates. The following examples will walk you through using the script.

To interactively view the expiration dates and registrars for a batch of domains you can run the script with the "--interactive
" option:
<pre>
$ dns-domain-expiration-checker.py --interactive --domainfile domains
Domain Name                Registrar                       Expiration Date       Days Left
prefetch.net               DNC HOLDINGS, INC.              2020-06-23 00:00:00   1064
spotch.com                 GANDI SAS                       2017-12-03 00:00:00   131 
google.com                 MARKMONITOR INC.                2020-09-14 00:00:00   1147
</pre>

To generate an e-mail when a domain is about to expire you can pass a single domain nad threshold to the script:

$ dns-domain-expiration-checker.py --domainname prefetch.net --email --expiredays 2000

Or you can define multiple domains in a file and pass that as an argument:

<pre>
$ cat domains
spotch.com 60
yahoo.com 60
prefetch.net 2000
google.com 80

$ dns-domain-expiration-checker.py --domainfile domains --email --smtpserver smtp.mydomain --smtpto "biff" --smtpfrom "Root"
</pre>

# Installation

The dns-domain-expiration-checker.py script uses the Python whois module to retrieve whois data. The version that is currently in PiPy has a number of issues which prevent it from parsing several registrar's WHOIS data. Fortunately Andrew Minkin fork'ed the original code and modified it to work with the dates from various registrars. To get the most out of the script I would highly suggest pulling down Andrew's code. Here are the steps to do this:

1. Create a virtualenv to run dns-domain-expiration-checker in:
<pre>
$ mkproject dns-domain-expiration-checker
</pre>
2. Surf over to that new environment:
<pre>
$ workon dns-domain-expiration-checker
</pre>
3. Pull down Andrew's updated module:
<pre>
$ pip install git+git://github.com/gen1us2k/python-whois.git
</pre>
4. Clone this repo to gget the script:
<pre>
$ git clone https://github.com/Matty9191/dns-domain-expiration-checker.git
</pre>
5. Run the script against the domains you want to check (this assume you are in the root of your virtualenv):
<pre>
$ ns-domain-expiration-checker/ns-domain-expiration-checker.py ....
</pre>
6. Automate this process.

Now if you are feeling frisky you can install the Python whois module from your favorite remote repository (available through apt, yum and pip) and skip steps 1 - 3. If you get a "Unknown date format" message when you run it you will need to install the newer Python whois module. This contains several enhancements to the DATA_FORMAT array in the adjust.py file.




