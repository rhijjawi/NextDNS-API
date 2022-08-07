import requests
import json
from json import JSONDecodeError
import os
from pathlib import Path

nativetracking = ["sonos", "xiaomi", "apple", "windows", "huawei", "samsung", "alexa", "roku"]

blocksites = [
    "tiktok",
    "tinder",
    "facebook",
    "snapchat",
    "instagram",
    "fortnite",
    "messenger",
    "leagueoflegends",
    "9gag",
    "tumblr",
    "vk",
    "roblox",
    "twitch",
    "minecraft",
    "pinterest",
    "discord",
    "twitter",
    "dailymotion",
    "whatsapp",
    "steam",
    "youtube",
    "hulu",
    "reddit",
    "blizzard",
    "netflix",
    "imgur",
    "vimeo",
    "disney+",
    "telegram",
    "skype",
    "ebay",
    "spotify",
    "amazon",
    "zoom",
    "primevideo",
    "xboxlive",
    "signal"]

headers = {
    """Accept""": """application/json, text/plain, */*""",
    """Accept-Language""": """en-US,en;q=0.5""",
    """Content-Type""": """application/json""",
    """Origin""": """https://my.nextdns.io""",
    """DNT""": """1""",
    """Connection""": """keep-alive""",
    """Referer""": """https://my.nextdns.io/""",
    """Sec-Fetch-Dest""": """empty""",
    """Sec-Fetch-Mode""": """cors""",
    """Sec-Fetch-Site""": """same-site""",
    """Sec-GPC""": """1""",
    """TE""": """trailers""",
}


class NoCredentials(Exception):
    def __init__(self, message="No credentials in account.login() function. Login using account.login(email,password)"):
        self.message = message
        super().__init__(self.message)


class NewAccount(Exception):
    def __init__(self,
                 message="No credentials in account.signup() function. Login using account.signup(email,password)"):
        self.message = message
        super().__init__(self.message)


class FailedCredentials(Exception):
    def __init__(self, error):
        self.error = error
        if error == """{"errors":{"code":"invalid"}}""":
            self.message = f"2FA code invalid. Please check credentials, login using account.login(email,password) and enter the correct 2FA code"
        else:
            self.message = f"Credentials in account.login() function failed. Please check credentials and login using account.login(email,password)\nError: {error}"
        super().__init__(self.message)


class OptionUnavailable(Exception):
    def __init__(self, allowed, message="Supplied option is unavailable, probably cause it does not exist"):
        self.allowed = allowed
        self.message = message
        super().__init__(self.message)


class ConfigNotFound(Exception):
    def __init__(self, config):
        self.config = config
        self.message = f"Config {config} cannot be found, probably cause it does not exist"
        super().__init__(self.message)


class account:
    def signup(email: str = None, password: str = None):
        if (email == None or password == None) or (email == None and password == None):
            raise NewAccount
        else:
            json = {"email": f"{email}", "password": f"{password}"}
            signup = requests.post('https://api.nextdns.io/accounts/@login', headers=headers, json=json)
            if signup.text == "OK":
                return "OK"
            else:
                return signup.text

    def login(email: str = None, password: str = None, otp: str = None):
        if (email == None or password == None) or (email == None and password == None):
            raise NoCredentials
        else:
            success = False
            json = {"email": f"{email}", "password": f"{password}"}
            while success == False:
                login = requests.post('https://api.nextdns.io/accounts/@login', headers=headers, json=json)
                if login.text == "OK":
                    success = 1
                elif login.text == """{"requiresCode":true}""":
                    code = otp or input("""Please enter 2FA Code: """)
                    json = {"email": f"{email}", "password": f"{password}", "code": f"{code}"}
                    login = requests.post('https://api.nextdns.io/accounts/@login', headers=headers, json=json)
                else:
                    raise FailedCredentials(login.text)
            c = login.cookies.get_dict()
            c = c['pst']
            headers['Cookie'] = f'pst={c}'
        return headers

    def list(header):
        configs = requests.get("https://api.nextdns.io/accounts/@me?withConfigurations=true", headers=header)
        configs = configs.json()
        confs = configs['configurations']
        return confs

    def month(header):
        month = requests.get(f"https://api.nextdns.io/accounts/@me/usage", headers=header)
        month = month.json()
        return month


class settings:
    def listsettings(config, header):
        list = requests.get(f"https://api.nextdns.io/profiles/{config}/settings", headers=header)
        if list.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            list = list.json()
            return list

    def setup(config, header):
        setup = requests.get(f"https://api.nextdns.io/profiles/{config}/setup", headers=header)
        print(setup.text)
        if setup.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            setup = setup.json()
            return setup

    def downloadlogs(config, header):
        downloads_path = str(Path.home() / "Downloads")
        fname = config + '.csv'  # official nextdns nomenclature
        file_path = os.path.join(downloads_path, fname)
        file = open(file_path, "wb")
        r = requests.get(f"https://api.nextdns.io/profiles/{config}/logs/download/", headers=header,
                         stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            file.write(chunk)
        return fname

    def clearlogs(config, header):
        logs = requests.delete(f"https://api.nextdns.io/profiles/{config}/logs", headers=header)
        if logs.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logs.text

    def rename(name, config, header):
        nname = {"name": name}
        rename = requests.patch(f"https://api.nextdns.io/profiles/{config}", headers=header, json=nname)
        if rename.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return f"Config renamed to {name}"

    def delete(config, header):
        dconfig = requests.delete(f"https://api.nextdns.io/profiles/{config}", headers=header)
        if dconfig.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return f"Config {config} deleted"

    def logclientips(bool, config, header):
        if bool == True:
            bool = False
        else:
            bool = True
        logcips = {"ip": bool}
        logcips = requests.patch(f"https://api.nextdns.io/profiles/{config}/settings/logs/drop", headers=header,
                                 json=logcips)
        if logcips.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logcips.text

    def logdomains(bool, config, header):
        if bool == True:
            bool = False
        else:
            bool = True
        logdom = {"domain": bool}
        logdom = requests.patch(f"https://api.nextdns.io/profiles/{config}/settings/logs/drop", headers=header,
                                json=logdom)
        if logdom.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logdom.text

    def blockpage(bool, config, header):
        bp = {"enabled": bool}
        bp = requests.patch(f"https://api.nextdns.io/profiles/{config}/settings/blockPage", headers=header, json=bp)
        if bp.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return bp.text

    def updatelinkedip(config, header):
        r = settings.setup(config, header)
        updatetoken = r["data"]["linkedIp"]["updateToken"]
        updateip = requests.get(f"https://link-ip.nextdns.io/{config}/{updatetoken}")
        print(updateip.text)
        return updateip.text


class security:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/profiles/{config}/security", headers=header)
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings

    def threatintelligencefeeds(bool, config, header):
        setting = {"threatIntelligenceFeeds": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def aidetection(bool, config, header):
        setting = {"aiThreatDetection": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def safebrowsing(bool, config, header):
        setting = {"googleSafeBrowsing": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def cryptojacking(bool, config, header):
        setting = {"cryptojacking": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def dnsrebinding(bool, config, header):
        setting = {"dnsRebinding": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def homograph(bool, config, header):
        setting = {"idnHomographs": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def typosquatting(bool, config, header):
        setting = {"typosquatting": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def dga(bool, config, header):
        setting = {"dga": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def newdomains(bool, config, header):
        setting = {"nrd": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def dyndns(bool, config, header):
        setting = {"ddns": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def parked(bool, config, header):
        setting = {"parking": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def csam(bool, config, header):
        setting = {"csam": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/security", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def addtld(tld, config, header):
        data = {"id": tld}
        put = requests.post(f"https://api.nextdns.io/profiles/{config}/security/tlds",
                            headers=header, json=data)
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    def removetld(tld, config, header):
        remove = requests.delete(f"https://api.nextdns.io/profiles/{config}/security/tlds/{tld}",
                                 headers=header)
        if remove.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return remove.text


class privacy:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/profiles/{config}/privacy", headers=header)
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings

    def blockdisguised(bool, config, header):
        setting = {"disguisedTrackers": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/privacy", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def blockaffiliate(bool, config, header):
        setting = {"allowAffiliate": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/privacy", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def blocknative(native, config, header):
        if native in nativetracking:
            data = {"id": native}
            put = requests.post(f"https://api.nextdns.io/profiles/{config}/privacy/natives/", headers=header,
                                json=data)
            if put.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", nativetracking)
            return f"{native} is no valid parameter!"

    def unblocknative(native, config, header):
        if native in nativetracking:
            delete = requests.delete(f"https://api.nextdns.io/profiles/{config}/privacy/natives/{native}",
                                     headers=header)
            if delete.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", nativetracking)
            return f"{native} is no valid parameter!"


class parental:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/profiles/{config}/parentalcontrol", headers=header)
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings

    def porn(bool, config, header):
        if bool:
            data = {"id": "porn", "active": bool}
            setting = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                                    headers=header, json=data)
        else:
            setting = requests.delete(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/porn",
                                      headers=header)

        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def gambling(bool, config, header):
        if bool:
            data = {"id": "gambling", "active": bool}
            setting = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                                    headers=header, json=data)
        else:
            setting = requests.delete(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/gambling",
                                      headers=header)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def dating(bool, config, header):
        if bool:
            data = {"id": "dating", "active": bool}
            setting = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                                    headers=header, json=data)
        else:
            setting = requests.delete(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/dating",
                                      headers=header)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def piracy(bool, config, header):
        if bool:
            data = {"id": "piracy", "active": bool}
            setting = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                                    headers=header, json=data)
        else:
            setting = requests.delete(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/piracy",
                                      headers=header)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def socialnetworks(bool, config, header):
        if bool:
            data = {"id": "social-networks", "active": bool}
            setting = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                                    headers=header, json=data)
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/social-networks",
                headers=header)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def safesearch(bool, config, header):
        setting = {"safeSearch": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/parentalcontrol", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def youtubeRestrictedMode(bool, config, header):
        setting = {"youtubeRestrictedMode": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/parentalcontrol", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def blockbypass(bool, config, header):
        setting = {"blockBypass": bool}
        setting = requests.patch(f"https://api.nextdns.io/profiles/{config}/parentalcontrol", headers=header,
                                 json=setting)
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    def blocksite(site, config, header):
        if site in blocksites:
            data = {"id": site, "active": True}
            put = requests.post(f"https://api.nextdns.io/profiles/{config}/parentalcontrol/services/", headers=header,
                                json=data)
            if put.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", blocksites)
            return f"{site} is no valid parameter!"

    def unblocksite(site, config, header):
        if site in blocksites:
            delete = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/services/{site}", headers=header)
            if delete.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", blocksites)
            return f"{site} is no valid parameter!"


class denylist:
    def list(config, header):
        list = requests.get(f"https://api.nextdns.io/profiles/{config}/denylist", headers=header)
        if list.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            list = list.json()
            return list

    def blockdomain(domain, config, header):
        data = {"id": domain, "active": True}
        put = requests.post(f"https://api.nextdns.io/profiles/{config}/denylist/", headers=header, json=data)
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    def unblockdomain(domain, config, header):
        delete = requests.delete(f"https://api.nextdns.io/profiles/{config}/denylist/{domain}", headers=header)
        if delete.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return delete.text


class allowlist:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/profiles/{config}/allowlist", headers=header)
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return settings.json()

    def add(domain, config, header):
        data = {"id": domain, "active": True}
        put = requests.post(f"https://api.nextdns.io/profiles/{config}/allowlist/", headers=header, json=data)
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    def remove(domain, config, header):
        delete = requests.delete(f"https://api.nextdns.io/profiles/{config}/allowlist/{domain}", headers=header)
        if delete.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return delete.text


class analytics:
    def counter(config, header):
        count = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/status", headers=header)
        if count.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            count = count.json()
            return count

    def topresolveddomains(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=default",
                           headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def topblockeddomains(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=blocked",
                           headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def topalloweddomains(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=allowed", headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def topdevices(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/devices", headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def topclientips(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/ips", headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def toprootdomains(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/domains?root=true", headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top

    def gafam(config, header):
        gafam = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/destinations?type=gafam",
                             headers=header)
        if gafam.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = gafam.json()
            return top

    def trafficdest(config, header):
        top = requests.get(f"https://api.nextdns.io/profiles/{config}/analytics/destinations?type=countries",
                           headers=header)
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
