# Checking DNS DOmain Expiration

If you are here you may have had a domain expire and dealt with the annoyances that go with reclaiming it. It's no fun is it? To prevent yourself from dealing with this again you can install and run dns-domain-expiration-checker to monitor your domains. The script is easy to install and will send you an e-mail if your domain is set to expire. If you have a single domain to monitor you can run the following:
<pre>
$ dns-domain-expiration-checker.py--smtpserver smtp.mydomain --smtpto "biff" --smtpfrom "Root" --domainname prefetch.net --expiredays 60
</pre>
If you have numerous domains you can cretae a domain file and pass that as an argument:
<pre>
$ cat domains
spotch.com 60
yahoo.com 60
prefetch.net 2000
google.com 80

$ dns-domain-expiration-checker.py --domainfile domains --smtpserver smtp.mydomain --smtpto "biff" --smtpfrom "Root"
</pre>
