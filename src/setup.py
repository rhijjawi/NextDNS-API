from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
#wU2A6AagBtZSyEm
setup(
    name='nextdnsapi',
    packages=find_packages(include=['nextdnsapi']),
    version = '1.7.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="I was getting increasingly frustrated with NextDNS's lack of API. I wanted to manage things on the fly. So, I did the most logical thing. I built a python script (library-to-be) to control my NextDNS account. I decided to make it public because why not?",
    author_email = 'erpihmisr@relay.firefox.com',      # Type in your E-Mail
    url = 'https://github.com/rhijjawi/NextDNS-API',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/rhijjawi/NextDNS-API/archivev1-7-0.tar.gz',    # I explain this later on
    keywords = ['NEXTDNS', 'API', 'REQUESTS'],   # Keywords that define your package best
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[            # I get to this in a second
           'requests',
       ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    )