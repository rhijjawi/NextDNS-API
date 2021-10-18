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

### Table Of Contents

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

### About The Project

I was getting increasingly frustrated with NextDNS's lack of API. I wanted to manage things on the fly. So, I did the most logical thing. I built a python script (library-to-be) to control my NextDNS account. I decided to make it public because why not?

### Built With

Built using Python:

* Requests library

#### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* requests

```
pip install requests
```

#### Installation

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

### Usage

Usage is very easy, so I won't bother to go into the intricacies of the library, but I will go over some basic info. This library closely imitates the website.

#### Account

```python
header = account.login("example@example.com", "password123")
print(account.list(header))
#[{'id': '19nd7x', 'name': 'first config'}, {'id': '837xh82', 'name': 'other one'}]
```

#### Settings

```python
settings.listsettings(config,header)
settings.setup(config,header)
settings.clearlogs(config,header)
settings.rename(name, config, header)
settings.logclientips(bool, config, header)
settings.logdomains(bool, config, header)
settings.blockpage(bool, config, header)
settings.updatelinkedip(config,header)
```

#### Security

```python
security.list(config, header)
security.threatintelligencefeeds(bool, config, header)
security.aidetection(bool, config, header)
security.safebrowsing(bool, config, header)
security.cryptojacking(bool, config, header)
security.dnsrebinding(bool, config, header)
security.homograph(bool, config, header)
security.typosquatting(bool, config, header)
security.dga(bool, config, header)
security.newdomains(bool, config, header)
security.parked(bool, config, header)
security.csam(bool, config, header)
security.addtld(tld, config, header)
security.removetld(tld, config, header)
```

#### Privacy

```python
privacy.list(config, header)
privacy.blockdisguised(bool, config, header):
privacy.blockaffiliate(bool, config, header):
privacy.blocknative(native, config, header):
privacy.unblocknative(native, config, header):
```

#### Parental

#### Denylist

#### Allowlist

#### Analytics

### Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/rhijjawi/NextDNS-API/issues/new) to discuss it, or directly create a pull request after you edit the _README.md_ file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](CODE\_OF\_CONDUCT.md) before posting your first idea as well.

#### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for more information.

### Authors

* **Ramzi Hijjawi** - _Avid Python Developer_ - [Ramzi Hijjawi](https://github.com/rhijjawi/) - _Created the API_

### Acknowledgements

* [NextDNS - For making it almost too easy to interface with their control panel](https://www.nextdns.io)
* [Ramzi Hijjawi](https://github.com/rhijjawi)
