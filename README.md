# README

\


[![Logo](https://nextdns.io/favicon.ico)](https://github.com/rhijjawi/NextDNS-API)

#### NextDNS-API

An awesome way to interface with your NextDNS account - via Python!\
\
[**Explore the docs »**](https://github.com/rhijjawi/NextDNS-API)\
\
[Report Bug](https://github.com/rhijjawi/NextDNS-API/issues) . [Request Feature](https://github.com/rhijjawi/NextDNS-API/issues)

![Contributors](https://img.shields.io/github/contributors/rhijjawi/NextDNS-API?color=dark-green) ![Issues](https://img.shields.io/github/issues/rhijjawi/NextDNS-API) ![License](https://img.shields.io/github/license/rhijjawi/NextDNS-API)

#### Table Of Contents

* [About the Project](./#about-the-project)
* [Built With](./#built-with)
* [Getting Started](./#getting-started)
  * [Prerequisites](./#prerequisites)
  * [Installation](./#installation)
* [Usage](./#usage)
* [Contributing](./#contributing)
* [License](./#license)
* [Authors](./#authors)
* [Acknowledgements](./#acknowledgements)

#### About The Project

I was getting increasingly frustrated with NextDNS's lack of API. I wanted to manage things on the fly. So, I did the most logical thing. I built a python script (library-to-be) to control my NextDNS account. I decided to make it public because why not?

#### Built With

Built using Python:

* Requests library

**Prerequisites**

This is an example of how to list things you need to use the software and how to install them.

* requests

```
pip install requests
```

**Installation**

1. pip install nextdnsapi
2. Open your IDE
3. Import library

```py
from nextdnsapi.api import *
```

or

```py
from nextdnsapi import api
from api import *
```

1. Check [Github](https://github.com/rhijjawi/NextDNS-API) for Usage

#### Usage

Usage is very easy, so I won't bother to go into the intricacies of the library, but I will go over some basic info. This library closely imitates the website.

**Account**

```python
header = account.login("example@example.com", "password123")
print(account.list(header))
#[{'id': '19nd7x', 'name': 'first config'}, {'id': '837xh82', 'name': 'other one'}]
```

**Settings**

```python
settings.listsettings(config,header):
    #This command returns what settings are enabled for the provided config.
    Example: settings.listsettings("d46a5a", header)
    Response: {'name': 'Config 1', 'logging': True, 'logging_disable_query': False, 'logging_disable_client': False, 'logging_retention': 164200, 'logging_location': 'ch', 'blockPage': True, 'ecs': True, 'cacheBoost': True, 'cnameFlattening': True, 'handshake': True, 'rewrites': []}
settings.setup(config,header)
    #This command returns the setup information the provided config.
    Example: settings.setup("d46a5a", header)
    Response: {'id': 'd46a5a', 'fingerprint': 'fpd7527ea9b798****', 'ipv4': [], 'ipv6': ['2a07:****::**:6a5a', '2a07:****::**:6a5a'], 'linkedIpDNSServers': ['45.90.**.105', '45.90.**.105'], 'ddnsHostname': '****.ddns.net', 'linkedIpUpdateToken': 'd1aa9fe86e9c****', 'linkedIp': '41.210.***.69', 'dnsStamp': 'sdns://AgE*********CjQ1LjkwLjI4LjAADmRucy5uZXh0ZG5zLmlvBy9kNDZhNWE'}
settings.clearlogs(config,header)
    #This command clears the DNS logs for the provided config.
    Example: settings.clearlogs("d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
settings.rename(name, config, header)
    #This command renames the config.
    Example: settings.rename("Config One", "d46a5a", header)
    Response: "Response renamed to {new name}" if success, else ConfigNotFound
settings.logclientips(bool, config, header)
    #This command tells NextDNS whether or not it should log client IPs.
    Example: settings.logclientips(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
settings.logdomains(bool, config, header)
    #This command tells NextDNS whether or not it should log domains.
    Example: settings.logdomains(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
settings.blockpage(bool, config, header)
    #This command tells NextDNS whether or not it should enable the block page.
    Example: settings.blockpage(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
settings.updatelinkedip(config,header)
    #This command tells update the linked IP on NextDNS to your current IP.
    Example: settings.updatelinkedip(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
settings.delete(config, header)
    #This command renames the config.
    Example: settings.rename("d46a5a", header)
    Response: "{Config ID} deleted" if success, else ConfigNotFound
```

**Security**

```python
security.list(config, header)
    #This command lists current "Security" options on NextDNS.
    Example: security.list("d46a5a", header)
    Response: {'threatIntelligenceFeeds': True, 'aiThreatDetection': True, 'googleSafeBrowsing': False, 'cryptojacking': True, 'dnsRebinding': False, 'homograph': True, 'typosquatting': True, 'dga': True, 'nrd': False, 'parked': False, 'csam': True, 'blocked_tlds': []}
security.threatintelligencefeeds(bool, config, header)
    #This command tells NextDNS whether or not it should use Real-Time Threat Intelligence Feeds.
    Example: security.threatintelligencefeeds(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.aidetection(bool, config, header)
    #This command tells NextDNS whether or not it should use AI Threat Detection.
    Example: security.aidetection(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.safebrowsing(bool, config, header)
    #This command tells NextDNS whether or not it should force Google to display SafeSearch results only.
    Example: security.safebrowsing(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.cryptojacking(bool, config, header)
    #This command tells NextDNS whether or not it should block the unauthorized use of your device to mine cryptocurrency..
    Example: security.cryptojacking(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.dnsrebinding(bool, config, header)
    #This command tells NextDNS whether or not it should prevent attackers from taking control of your local devices through the Internet by automatically blocking DNS responses containing private IP addresses.
    Example: security.dnsrebinding(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.homograph(bool, config, header)
    #This command tells NextDNS whether or not it should block domains that impersonate other domains by abusing IDN registration. (Ex: replacing the Latin letter "e" with the Cyrillic letter "е".)
    Example: security.homograph(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.typosquatting(bool, config, header)
    #This command tells NextDNS whether or not it should block domains that target users who incorrectly type a website address.
    Example: security.typosquatting(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.dga(bool, config, header)
    #This command tells NextDNS whether or not it should use block domains generated by algorithms for rendezvous points for malware.
    Example: security.dga(True, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.newdomains(bool, config, header)
    #This command tells NextDNS whether or not it should block domains registered less than 30 days ago. 
    Example: security.newdomains(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.parked(bool, config, header)
    #This command tells NextDNS whether or not it should block pages laden with ads and devoid of any value.
    Example: security.parked(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.csam(bool, config, header)
    #This command tells NextDNS whether or not it should block domains hosting child sexual abuse material.
    Example: security.csam(False, "d46a5a", header)
    Response: "OK" if success, else ConfigNotFound
security.addtld(tld, config, header)
    #This command tells NextDNS to add the specified TLD to a blocklist.
    Example: security.addtld(".io", "d46a5a", header)
    Response: "{tld} blocked" if success, else ConfigNotFound
security.removetld(tld, config, header)
    #This command tells NextDNS to remove the specified TLD from a blocklist.
    Example: security.removetld(False, "d46a5a", header)
    Response: "{tld} unblocked" if success, else ConfigNotFound
```

**Privacy**

```python
privacy.list(config, header)
privacy.blockdisguised(bool, config, header):
privacy.blockaffiliate(bool, config, header):
privacy.blocknative(native, config, header):
privacy.unblocknative(native, config, header):
```

**Parental**

**Denylist**

**Allowlist**

**Analytics**

#### Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/rhijjawi/NextDNS-API/issues/new) to discuss it, or directly create a pull request after you edit the _README.md_ file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](CODE\_OF\_CONDUCT.md) before posting your first idea as well.

**Creating A Pull Request**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

#### License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

#### Authors

* **Ramzi Hijjawi** - _Avid Python Developer_ - [Ramzi Hijjawi](https://github.com/rhijjawi/) - _Created the API_

#### Acknowledgements

* [NextDNS - For making it almost too easy to interface with their control panel](https://www.nextdns.io)
* [Ramzi Hijjawi](https://github.com/rhijjawi)
