<br/>
<p align="center">
  <a href="https://github.com/rhijjawi/NextDNS-API">
    <img src="https://nextdns.io/favicon.ico" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NextDNS-API</h3>

  <p align="center">
    An awesome way to interface with your NextDNS account - via Python!
    <br/>
    <br/>
    <a href="https://github.com/rhijjawi/NextDNS-API"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/rhijjawi/NextDNS-API/issues">Report Bug</a>
    .
    <a href="https://github.com/rhijjawi/NextDNS-API/issues">Request Feature</a>
  </p>
</p>

![Contributors](https://img.shields.io/github/contributors/rhijjawi/NextDNS-API?color=dark-green) ![Issues](https://img.shields.io/github/issues/rhijjawi/NextDNS-API) ![License](https://img.shields.io/github/license/rhijjawi/NextDNS-API) 

## Table Of Contents

* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## About The Project

I was getting increasingly frustrated with NextDNS's lack of API. I wanted to manage things on the fly. So, I did the most logical thing. I built a python script (library-to-be) to control my NextDNS account. I decided to make it public because why not?

## Built With

Built using Python:
- Requests library 


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* requests

```sh
pip install requests
```

### Installation

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

4. Check [Github](https://github.com/rhijjawi/NextDNS-API) for Usage

## Usage

* account
  * account.login(email,password) assign this function to be a variable, as this function returns the headers neccessary to login to NextDNS via Python.
  * account.list(header)

_For more examples, please refer to the [Documentation](https://example.com)_

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/rhijjawi/NextDNS-API/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/rhijjawi/NextDNS-API/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/rhijjawi/NextDNS-API/blob/main/LICENSE.md) for more information.

## Authors

* **Ramzi Hijjawi** - *Avid Python Developer* - [Ramzi Hijjawi](https://github.com/rhijjawi/) - *Created the API*

## Acknowledgements

* [NextDNS - For making it almost too easy to interface with their control panel](https://www.nextdns.io)
* [Ramzi Hijjawi](https://github.com/rhijjawi)
