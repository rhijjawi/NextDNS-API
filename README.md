<p align="center">
  <a href="https://github.com/rhijjawi/NextDNS-API">
    <img src="https://nextdns.io/favicon.ico" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NextDNS-API</h3>

  <p align="center">
    An awesome way to interface with your NextDNS account - via Python!
    <br/>
    <br/>
    <a href="https://ramzihijjawi.gitbook.io/nextdns-api/"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/rhijjawi/NextDNS-API/issues">Report Bug</a>
    .
    <a href="https://github.com/rhijjawi/NextDNS-API/issues">Request Feature</a>
  </p>
</p>

![Contributors](https://img.shields.io/github/contributors/rhijjawi/NextDNS-API?color=dark-green) ![Issues](https://img.shields.io/github/issues/rhijjawi/NextDNS-API) ![License](https://img.shields.io/github/license/rhijjawi/NextDNS-API) [![Downloads](https://pepy.tech/badge/nextdnsapi)](https://pepy.tech/project/nextdnsapi) [![Downloads](https://pepy.tech/badge/nextdnsapi/month)](https://pepy.tech/project/nextdnsapi) [![Downloads](https://pepy.tech/badge/nextdnsapi/week)](https://pepy.tech/project/nextdnsapi)

#### Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Account](#account)
  * [Settings](#settings)
  * [Security](#security)
  * [Privacy](#privacy)
  * [Parental](#parental)
  * [Denylist](#denylist)
  * [Allowlist](#allowlist)
  * [Analytics](#analytics)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

#### About The Project

I was getting increasingly frustrated with NextDNS's lack of API. I wanted to manage things on the fly. So, I did the most logical thing. I built a python script (library-to-be) to control my NextDNS account. I decided to make it public because why not?

#### Built With

Built using Python:

* Requests library

##### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* requests



##### Installation

1. **```pip install nextdnsapi```**

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

##### Account

For logging in using 2FA, see [2FA.md](2FA.md)
```python
header = account.login("example@example.com", "password123")

account.login(email, password)
    #This command logs into NextDNS for you and stores authentication in the variable header.
    Example: account.login("example@example.com", "password123")
    Response: Login credentials (headers and cookies) for NextDNS
account.list(header)
    #This command lists the configurations available on your NextDNS account
    Example: account.list(header)
    Response: #[{'id': 'd46a5b', 'name': 'Config 1'}, {'id': '837xh82', 'name': 'other one'}]
account.month(header)
    #This command returns the number of queries made in the current month
    Example: account.month(header)
    Response: {"monthlyQueries":44065}
```

##### Settings

```python
settings.listsettings(config,header):
    #This command returns what settings are enabled for the provided config.
    Example: settings.listsettings("d46a5b", header)
    Response: {'name': 'Config 1', 'logging': True, 'logging_disable_query': False, 'logging_disable_client': False, 'logging_retention': 164200, 'logging_location': 'ch', 'blockPage': True, 'ecs': True, 'cacheBoost': True, 'cnameFlattening': True, 'handshake': True, 'rewrites': []}
settings.setup(config,header)
    #This command returns the setup information the provided config.
    Example: settings.setup("d46a5b", header)
    Response: {'id': 'd46a5b', 'fingerprint': 'fpd7527ea9b798****', 'ipv4': [], 'ipv6': ['2a07:****::**:6a5a', '2a07:****::**:6a5a'], 'linkedIpDNSServers': ['45.90.**.105', '45.90.**.105'], 'ddnsHostname': '****.ddns.net', 'linkedIpUpdateToken': 'd1aa9fe86e9c****', 'linkedIp': '41.210.***.69', 'dnsStamp': 'sdns://AgE*********CjQ1LjkwLjI4LjAADmRucy5uZXh0ZG5zLmlvBy9kNDZhNWE'}
settings.downloadlogs(config,header)
    #This command downloads the DNS logs for the provided config to OS downloads folder and returns file name.
    Example: settings.downloadlogs("d46a5b", header)
    Response: "d46a5b-2022-05-21T11 30 26.867Z.csv" if success, else ConfigNotFound
settings.clearlogs(config,header)
    #This command clears the DNS logs for the provided config.
    Example: settings.clearlogs("d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.rename(name, config, header)
    #This command renames the config.
    Example: settings.rename("Config One", "d46a5b", header)
    Response: "Response renamed to {new name}" if success, else ConfigNotFound
settings.logclientips(bool, config, header)
    #This command tells NextDNS whether or not it should log client IPs.
    Example: settings.logclientips(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.logdomains(bool, config, header)
    #This command tells NextDNS whether or not it should log domains.
    Example: settings.logdomains(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.blockpage(bool, config, header)
    #This command tells NextDNS whether or not it should enable the block page.
    Example: settings.blockpage(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.adddnsrewrite(domain, answer, config, header)
    #This command tells NextDNS to create a DNS rewrite for the specific pairing.
    Example: settings.adddnsrewrite("router.local", "192.168.1.1", "d46a5b", header)
    Response: {"id":12345,"name":"router.local","answer":"192.168.1.1"} if success, else ConfigNotFound
settings.deletednsrewrite(id, config, header)
    #This command tells NextDNS to delete a DNS rewrite.
    Example: settings.deletednsrewrite(12345, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.updatelinkedip(config,header)
    #This command tells update the linked IP on NextDNS to your current IP.
    Example: settings.updatelinkedip(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
settings.delete(config, header)
    #This command renames the config.
    Example: settings.rename("d46a5b", header)
    Response: "{Config ID} deleted" if success, else ConfigNotFound
```

##### Security

```python
security.list(config, header)
    #This command lists current "Security" options on NextDNS.
    Example: security.list("d46a5b", header)
    Response: {'threatIntelligenceFeeds': True, 'aiThreatDetection': True, 'googleSafeBrowsing': False, 'cryptojacking': True, 'dnsRebinding': False, 'homograph': True, 'typosquatting': True, 'dga': True, 'nrd': False, 'parked': False, 'csam': True, 'blocked_tlds': []}
security.threatintelligencefeeds(bool, config, header)
    #This command tells NextDNS whether or not it should use Real-Time Threat Intelligence Feeds.
    Example: security.threatintelligencefeeds(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.aidetection(bool, config, header)
    #This command tells NextDNS whether or not it should use AI Threat Detection.
    Example: security.aidetection(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.safebrowsing(bool, config, header)
    #This command tells NextDNS whether or not it should block malware and phishing domains using Google Safe Browsing. (NOT SAFESEARCH)
    Example: security.safebrowsing(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.cryptojacking(bool, config, header)
    #This command tells NextDNS whether or not it should block the unauthorized use of your device to mine cryptocurrency..
    Example: security.cryptojacking(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.dnsrebinding(bool, config, header)
    #This command tells NextDNS whether or not it should prevent attackers from taking control of your local devices through the Internet by automatically blocking DNS responses containing private IP addresses.
    Example: security.dnsrebinding(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.homograph(bool, config, header)
    #This command tells NextDNS whether or not it should block domains that impersonate other domains by abusing IDN registration. (Ex: replacing the Latin letter "e" with the Cyrillic letter "е".)
    Example: security.homograph(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.typosquatting(bool, config, header)
    #This command tells NextDNS whether or not it should block domains that target users who incorrectly type a website address.
    Example: security.typosquatting(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.dga(bool, config, header)
    #This command tells NextDNS whether or not it should use block domains generated by algorithms for rendezvous points for malware.
    Example: security.dga(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.newdomains(bool, config, header)
    #This command tells NextDNS whether or not it should block domains registered less than 30 days ago. 
    Example: security.newdomains(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.parked(bool, config, header)
    #This command tells NextDNS whether or not it should block pages laden with ads and devoid of any value.
    Example: security.parked(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.csam(bool, config, header)
    #This command tells NextDNS whether or not it should block domains hosting child sexual abuse material.
    Example: security.csam(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
security.addtld(tld, config, header)
    #This command tells NextDNS to add the specified TLD to a blocklist.
    Example: security.addtld(".io", "d46a5b", header)
    Response: "{tld} blocked" if success, else ConfigNotFound
security.removetld(tld, config, header)
    #This command tells NextDNS to remove the specified TLD from a blocklist.
    Example: security.removetld(False, "d46a5b", header)
    Response: "{tld} unblocked" if success, else ConfigNotFound
```

##### Privacy

```python
privacy.list(config, header)
    #This command lists current "Privacy" options on NextDNS.
    Example: privacy.list("d46a5b", header)
    Response: {'blockDisguised': False, 'allowAffiliate': False, 'blocklists': [{'id': 'nextdns-recommended', 'name': None, 'website': None, 'description': None, 'entries': 95040, 'updatedOn': '2021-10-20T00:30:42.000Z'}], 'natives': [{'id': 'alexa'}, {'id': 'samsung'}]} if success, else ConfigNotFound
privacy.blockdisguised(bool, config, header):
    #This command tells NextDNS whether or not it should block third-party trackers disguising themselves as first-party.
    Example: security.csam(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
privacy.blockaffiliate(bool, config, header):
    #This command tells NextDNS whether or not it should block affiliate & tracking domains.
    Example: security.blockaffiliate(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
privacy.blocknative(native, config, header):
    #This command tells NextDNS to block the built-in native tracker of the specified company.
    Example: security.blockaffiliate("xiaomi", "d46a5b", header) #Options: ["sonos", "xiaomi", "apple", "windows", "huawei", "samsung", "alexa", "roku"]
    Response: "OK" if success, else ConfigNotFound
privacy.unblocknative(native, config, header):
    #This command tells NextDNS to unblock the built-in native tracker of the specified company.
    Example: security.unblocknative("sonos", "d46a5b", header) #Options: ["sonos", "xiaomi", "apple", "windows", "huawei", "samsung", "alexa", "roku"]
    Response: "OK" if success, else ConfigNotFound
```

##### Parental

```python
parental.list(config, header)
    #This command lists current "Privacy" options on NextDNS.
    Example: parental.list("d46a5b", header)
    Response: {'safeSearch': False, 'youtubeRestrictedMode': True, 'blockBypass': False, 'services': [{'id': 'instagram', 'website': 'https://www.instagram.com', 'recreation': False, 'active': True}], 'categories': [{'id': 'porn', 'recreation': False, 'active': True}], 'recreation': {'tuesday': {'start': '18:00:00', 'end': '20:30:00'}, 'wednesday': {'start': '18:00:00', 'end': '20:30:00'}, 'thursday': {'start': '18:00:00', 'end': '20:30:00'}, 'friday': {'start': '18:00:00', 'end': '20:30:00'}, 'saturday': {'start': '09:00:00', 'end': '20:30:00'}, 'sunday': {'start': '09:00:00', 'end': '20:30:00'}}} if success, else ConfigNotFound
parental.porn(bool, config, header)
    #This command tells NextDNS whether or not it should block Porn
    Example: parental.porn(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.gambling(bool, config, header)
    #This command tells NextDNS whether or not it should block sites related to Gambling
    Example: parental.gambling(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.dating(bool, config, header)
    #This command tells NextDNS whether or not it should block dating sites.
    Example: parental.dating(True, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.piracy(bool, config, header)
    #This command tells NextDNS whether or not it should block P2P websites, protocols, copyright-infringing streaming websites and generic video hosting websites used mainly for illegally distributing copyrighted content.
    Example: parental.piracy(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.socialnetworks(bool, config, header)
    #This command tells NextDNS whether or not it should block social networks sites and apps (Facebook, Instagram, TikTok, Reddit, etc.). Does not block messaging apps.
    Example: parental.socialnetworks(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.safesearch(bool, config, header)
    #This command tells NextDNS whether or not it should filter explicit results on all major search engines, including images and videos. This will also block access to search engines not supporting this feature.
    Example: parental.safesearch(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.youtubeRestrictedMode(bool, config, header)
    #This command tells NextDNS whether or not it should force YouTube Restricted Mode.
    Example: parental.youtubeRestrictedMode(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.blockbypass(bool, config, header)
    #This command tells NextDNS whether or not it should block bypass methods (VPNs, proxies, Tor-related software and encrypted DNS providers).
    Example: parental.blockbypass(False, "d46a5b", header)
    Response: "OK" if success, else ConfigNotFound
parental.blocksite(site, config, header)
    #This command tells NextDNS to block the specified site
    Example: parental.blocksite("Instagram", "d46a5b", header) #Options: ["tiktok","tinder","facebook","snapchat":,"instagram","fortnite","message","leagueoflegends","9gag","tumblr","vk","roblox","twitch","minecraft","pinterest","discord","twitter","dailymotion","whatsapp","steam","youtube","hulu","reddit","blizzard","netflix","imgur","vimeo","disney+","telegram","skype","ebay","spotify","amazon","zoom","primevideo"]
    Response: "OK" if success, else ConfigNotFound
parental.unblocksite(site, config, header)
    #This command tells NextDNS to block the specified site
    Example: parental.unblocksite("Snapchat", "d46a5b", header) #Options: ["tiktok","tinder","facebook","snapchat":,"instagram","fortnite","message","leagueoflegends","9gag","tumblr","vk","roblox","twitch","minecraft","pinterest","discord","twitter","dailymotion","whatsapp","steam","youtube","hulu","reddit","blizzard","netflix","imgur","vimeo","disney+","telegram","skype","ebay","spotify","amazon","zoom","primevideo"]
    Response: "OK" if success, else ConfigNotFound
```

##### Denylist

```python
denylist.list(config, header)
    #This command lists domains on the NextDNS denylist.
    Example: denylist.list("d46a5b", header)
    Response: [{'domain': 'krunker.io', 'active': True}] if success else ConfigNotFound
denylist.blockdomain(domain, config, header)
    #This command adds a domain to the NextDNS denylist.
    Example: denylist.blockdomain("krunker.io", "d46a5b", header)
    Response: "OK" if success else ConfigNotFound
denylist.unblockdomain(domain, config, header)
    #This command removes a domain from the NextDNS denylist.
    Example: parental.list("krunker.io", "d46a5b", header)
    Response: "OK" if success else ConfigNotFound
```

##### Allowlist

```python
allowlist.list(config, header)
    #This command lists current domains on the NextDNS denylist.
    Example: denylist.list("d46a5b", header)
    Response: [{'domain': 'example.com', 'active': True}] if success else ConfigNotFound
allowlist.add(domain, config, header)
    #This command adds a domain to the NextDNS whitelist.
    Example: allowlist.add("krunker.io", "d46a5b", header)
    Response: "OK" if success else ConfigNotFound
allowlist.remove(domain, config, header)
    #This command removes a domain from the NextDNS whitelist. (DOES NOT BLOCK, JUST REMOVES FROM WHITELIST)
    Example: allowlist.remove("krunker.io", "d46a5b", header)
    Response: "OK" if success else ConfigNotFound
```

##### Analytics

```python
analytics.counter(config, header)
    #This command returns the number of total queries and blocked queries.
    Example: analytics.counter("d46a5b", header)
    Response: {'queries': 6736, 'blockedQueries': 208} if success else ConfigNotFound
analytics.topresolveddomains(config, header)
    #This command returns the top resolved domains.
    Example: analytics.topresolveddomains("d46a5b", header)
    Response: [{'name': 'os-code.shalltry.com', 'queries': 61}, {'name': 'pull-f5.tiktokcdn.com', 'queries': 47}, {'name': 'pull-f5-tt01.fcdn.us.tiktokv.com', 'queries': 45}, {'name': 'pull-f5-va01.tiktokcdn.com', 'queries': 45}, {'name': 'clients3.google.com', 'queries': 45}, {'name': 'mqtt-mini.facebook.com', 'queries': 42}] if success else ConfigNotFound
analytics.topblockeddomains(config, header)
    #This command returns the top blocked domains.
    Example: analytics.topblockeddomains("d46a5b", header)
    Response: [{'name': 'graph.instagram.com', 'queries': 71}, {'name': 'i.instagram.com', 'queries': 34}, {'name': 'app-measurement.com', 'queries': 26}, {'name': 'www.googleadservices.com', 'queries': 20}, {'name': 'data.flurry.com', 'queries': 15}, {'name': 'googleads.g.doubleclick.net', 'queries': 11}] if success else ConfigNotFound
analytics.toplists(config, header)
    #This command returns the settings responsible for the most blocks.
    Example: analytics.toplists("d46a5b", header)
    Response: [{'name': 'Instagram', 'queries': 106}, {'name': 'NextDNS Ads & Trackers Blocklist', 'queries': 103}] if success else ConfigNotFound
analytics.topdevices(config, header)
    #This command returns the top devices issuing queries.
    Example: analytics.topdevices("d46a5b", header)
    Response: [{'id': '4SVEZ', 'queries': 6432, 'name': "John Appleseed's iPhone"}] if success else ConfigNotFound
analytics.topclientips(config, header)
    #This command returns the top IP addresses issuing queries.
    Example: analytics.topclientips("d46a5b", header)
    Response: [{'ip': '188.34.***.204', 'queries': 4680, 'isCellular': False, 'city': 'Gunzenhausen', 'country': 'Germany', 'countryCode': 'DE', 'isp': 'Hetzner Online GmbH'}, {'ip': '**.210.155.183', 'queries': 1752, 'isCellular': True, 'city': '*****', 'country': 'Timbuktu', 'countryCode': '**', 'isp': '***'}] if success else ConfigNotFound
analytics.toprootdomains(config, header)
    #This command returns the top root domains being accessed.
    Example: analytics.toprootdomains("d46a5b", header)
    Response: [{'name': 'tiktokcdn.com', 'queries': 3472}, {'name': 'ttlivecdn.com', 'queries': 1061}, {'name': 'tiktokv.com', 'queries': 416}, {'name': 'gstatic.com', 'queries': 236}, {'name': 'facebook.com', 'queries': 152}, {'name': 'shalltry.com', 'queries': 150}] if success else ConfigNotFound
analytics.gafam(config, header)
    #This command returns the GAFAM distrubution of traffic (Google, Apple, Facebook, Amazon and Microsoft).
    Example: analytics.gafam("d46a5b", header)
    Response: [{'company': 'google', 'queries': 622, 'percentage': 0.09670398009950248}, {'company': 'facebook', 'queries': 472, 'percentage': 0.07338308457711443}, {'company': 'amazon', 'queries': 0, 'percentage': 0}, {'company': 'apple', 'queries': 0, 'percentage': 0}, {'company': 'microsoft', 'queries': 0, 'percentage': 0}, {'company': 'others', 'queries': 5338, 'percentage': 0.8299129353233831}] if success else ConfigNotFound
analytics.trafficdest(config, header)
    #This command returns the top destinations of query traffic.
    Example: analytics.trafficdest("d46a5b", header)
    Response: {'DE': {'queries': 3097, 'topDomains': ['mqtt-mini.facebook.com', 'pull-hls-l1-sg01.ttlivecdn.com', 'pull-hls-f1-ab.tiktokcdn.com', 'pull-hls-l1-sg01.tiktokcdn.com', 'pull-hls-f1-sg01.tiktokcdn.com']}, 'US': {'queries': 691, 'topDomains': ['clients3.google.com', 'mtalk.google.com', 'frontier-va.tiktokv.com', 'pull-f5-va01.tiktokcdn.com', 'log22-normal-useast1a.tiktokv.com']}, 'IE': {'queries': 198, 'topDomains': ['os-code.shalltry.com', 'aireport.shalltry.com', 'ds.shalltry.com', 'af.shalltry.com', 'ire-dsu.shalltry.com']}} if success else ConfigNotFound
```

#### Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/rhijjawi/NextDNS-API/issues/new) to discuss it, or directly create a pull request after you edit the _README.md_ file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](CODE\_OF\_CONDUCT.md) before posting your first idea as well.

##### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

#### License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

#### Authors

* [Ramzi Hijjawi](https://github.com/rhijjawi/) (_Avid Python Developer_) - _Created the API_

#### Acknowledgements

* [NextDNS - For making it almost too easy to interface with their control panel](https://www.nextdns.io)
* [Ramzi Hijjawi](https://github.com/rhijjawi)
* [Jin Kang](https://github.com/jinkang23) - For helping fix build issues and reformatting the GitHub to be more user friendly
* [David Desrosiers](https://github.com/desrod) - For adding Postman documentation
