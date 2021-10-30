# Setting up 2FA for NextDNS API
1. If 2FA is already enabled on your account, please disable it. (It will be re-enabled later.)
2. Install a time-based authenticator such as Authy or Google Authenticator.
3. Visit [2FA settings](https://my.nextdns.io/account)
4. Enable 2FA and copy the text **below** the QR code.
5. Save this as a variable, such as ```qrbase```
6. Install ```pyotp``` using: ```pip install pyotp```
7. Use it like so:
```py
from nextdnsapi.api import *
import pyotp

totp = pyotp.TOTP(base)
totp_code = totp.now()
print(totp_code)
header = account.login("user@example.com", "password123", totp_code)```
