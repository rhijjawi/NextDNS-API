import os
from pathlib import Path

import requests

nativetracking = [
    "sonos",
    "xiaomi",
    "apple",
    "windows",
    "huawei",
    "samsung",
    "alexa",
    "roku",
]

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
    "signal",
]

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Origin": "https://my.nextdns.io",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://my.nextdns.io/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-GPC": "1",
    "TE": "trailers",
}


class NoCredentials(Exception):
    def __init__(
        self,
        message="No credentials in account.login() function. Login using account.login(email,password)",
    ):
        self.message = message
        super().__init__(self.message)


class NewAccount(Exception):
    def __init__(
        self,
        message="No credentials in account.signup() function. Login using account.signup(email,password)",
    ):
        self.message = message
        super().__init__(self.message)


class FailedCredentials(Exception):
    def __init__(self, error):
        self.error = error
        if error == """{"errors":{"code":"invalid"}}""":
            self.message = "2FA code invalid. Please check credentials, login using account.login(email,password) and enter the correct 2FA code"
        else:
            self.message = f"Credentials in account.login() function failed. Please check credentials and login using account.login(email,password)\nError: {error}"
        super().__init__(self.message)


class OptionUnavailable(Exception):
    def __init__(
        self,
        allowed,
        message="Supplied option is unavailable, probably cause it does not exist",
    ):
        self.allowed = allowed
        self.message = message
        super().__init__(self.message)


class ConfigNotFound(Exception):
    def __init__(self, config):
        self.config = config
        self.message = (
            f"Config {config} cannot be found, probably cause it does not exist"
        )
        super().__init__(self.message)


class account:
    @staticmethod
    def signup(email: str = "", password: str = ""):
        if not email or not password:
            raise NewAccount

        json_data = {"email": email, "password": password}
        signup = requests.post(
            "https://api.nextdns.io/accounts/@login", headers=headers, json=json_data
        )
        return "OK" if signup.text == "OK" else signup.text

    @staticmethod
    def login(email: str = "", password: str = "", otp: str = ""):
        if not email or not password:
            raise NoCredentials

        success = False
        json_data = {"email": email, "password": password}
        while not success:
            login = requests.post(
                "https://api.nextdns.io/accounts/@login",
                headers=headers,
                json=json_data,
            )
            if login.text == "OK":
                success = True
            elif login.text == """{"requiresCode":true}""":
                code = otp or input("Please enter 2FA Code: ")
                json_data = {"email": email, "password": password, "code": code}
                login = requests.post(
                    "https://api.nextdns.io/accounts/@login",
                    headers=headers,
                    json=json_data,
                )
            else:
                raise FailedCredentials(login.text)
        c = login.cookies.get_dict()
        c = c["pst"]
        headers["Cookie"] = f"pst={c}"
        return headers

    @staticmethod
    def list(header):
        configs = requests.get(
            "https://api.nextdns.io/accounts/@me?withConfigurations=true",
            headers=header,
        )
        configs = configs.json()
        return configs["configurations"]

    @staticmethod
    def month(header):
        month = requests.get(
            "https://api.nextdns.io/accounts/@me/usage", headers=header
        )
        month = month.json()
        return month


class settings:
    @staticmethod
    def listsettings(config, header):
        response = requests.get(
            f"https://api.nextdns.io/profiles/{config}/settings", headers=header
        )
        if response.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        response = response.json()
        return response

    @staticmethod
    def setup(config, header):
        setup = requests.get(
            f"https://api.nextdns.io/profiles/{config}/setup", headers=header
        )
        print(setup.text)
        if setup.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        setup = setup.json()
        return setup

    @staticmethod
    def downloadlogs(config, header):
        downloads_path = str(Path.home() / "Downloads")
        fname = f"{config}.csv"
        file_path = os.path.join(downloads_path, fname)
        file = open(file_path, "wb")
        r = requests.get(
            f"https://api.nextdns.io/profiles/{config}/logs/download/",
            headers=header,
            stream=True,
        )
        for chunk in r.iter_content(chunk_size=1024):
            file.write(chunk)
        return fname

    @staticmethod
    def clearlogs(config, header):
        logs = requests.delete(
            f"https://api.nextdns.io/profiles/{config}/logs", headers=header
        )
        if logs.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logs.text

    @staticmethod
    def rename(name, config, header):
        nname = {"name": name}
        rename = requests.patch(
            f"https://api.nextdns.io/profiles/{config}", headers=header, json=nname
        )
        if rename.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return f"Config renamed to {name}"

    @staticmethod
    def delete(config, header):
        dconfig = requests.delete(
            f"https://api.nextdns.io/profiles/{config}", headers=header
        )
        if dconfig.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return f"Config {config} deleted"

    @staticmethod
    def logclientips(ip, config, header):
        ip = ip is not True
        logcips = {"ip": ip}
        logcips = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/settings/logs/drop",
            headers=header,
            json=logcips,
        )
        if logcips.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logcips.text

    @staticmethod
    def logdomains(domain, config, header):
        domain = domain is not True
        logdom = {"domain": domain}
        logdom = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/settings/logs/drop",
            headers=header,
            json=logdom,
        )
        if logdom.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return logdom.text

    @staticmethod
    def blockpage(enabled, config, header):
        bp = {"enabled": enabled}
        bp = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/settings/blockPage",
            headers=header,
            json=bp,
        )
        if bp.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return bp.text

    @staticmethod
    def updatelinkedip(config, header):
        r = settings.setup(config, header)
        updatetoken = r["data"]["linkedIp"]["updateToken"]
        updateip = requests.get(f"https://link-ip.nextdns.io/{config}/{updatetoken}")
        print(updateip.text)
        return updateip.text


class security:
    @staticmethod
    def list(config, header):
        settings = requests.get(
            f"https://api.nextdns.io/profiles/{config}/security", headers=header
        )
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        settings = settings.json()
        return settings

    @staticmethod
    def threatintelligencefeeds(threatIntelligenceFeeds, config, header):
        setting = {"threatIntelligenceFeeds": threatIntelligenceFeeds}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def aidetection(aiThreatDetection, config, header):
        setting = {"aiThreatDetection": aiThreatDetection}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def safebrowsing(googleSafeBrowsing, config, header):
        setting = {"googleSafeBrowsing": googleSafeBrowsing}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def cryptojacking(cryptojacking, config, header):
        setting = {"cryptojacking": cryptojacking}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def dnsrebinding(dnsRebinding, config, header):
        setting = {"dnsRebinding": dnsRebinding}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def homograph(idnHomographs, config, header):
        setting = {"idnHomographs": idnHomographs}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def typosquatting(typosquatting, config, header):
        setting = {"typosquatting": typosquatting}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def dga(dga, config, header):
        setting = {"dga": dga}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def newdomains(nrd, config, header):
        setting = {"nrd": nrd}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def dyndns(ddns, config, header):
        setting = {"ddns": ddns}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def parked(parking, config, header):
        setting = {"parking": parking}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def csam(csam, config, header):
        setting = {"csam": csam}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/security",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def addtld(tld, config, header):
        data = {"id": tld}
        put = requests.post(
            f"https://api.nextdns.io/profiles/{config}/security/tlds",
            headers=header,
            json=data,
        )
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    @staticmethod
    def removetld(tld, config, header):
        remove = requests.delete(
            f"https://api.nextdns.io/profiles/{config}/security/tlds/{tld}",
            headers=header,
        )
        if remove.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return remove.text


class privacy:
    @staticmethod
    def list(config, header):
        settings = requests.get(
            f"https://api.nextdns.io/profiles/{config}/privacy", headers=header
        )
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        settings = settings.json()
        return settings

    @staticmethod
    def blockdisguised(disguisedTrackers, config, header):
        setting = {"disguisedTrackers": disguisedTrackers}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/privacy",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def blockaffiliate(allowAffiliate, config, header):
        setting = {"allowAffiliate": allowAffiliate}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/privacy",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def blocknative(native, config, header):
        if native in nativetracking:
            data = {"id": native}
            put = requests.post(
                f"https://api.nextdns.io/profiles/{config}/privacy/natives/",
                headers=header,
                json=data,
            )
            if put.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", nativetracking)
            return f"{native} is no valid parameter!"

    @staticmethod
    def unblocknative(native, config, header):
        if native in nativetracking:
            delete = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/privacy/natives/{native}",
                headers=header,
            )
            if delete.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", nativetracking)
            return f"{native} is no valid parameter!"


class parental:
    @staticmethod
    # TODO: Change the method name from `list` to something different
    def list(config, header):
        settings = requests.get(
            f"https://api.nextdns.io/profiles/{config}/parentalcontrol", headers=header
        )
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        settings = settings.json()
        return settings

    @staticmethod
    def porn(active, config, header):
        if active:
            data = {"id": "porn", "active": active}
            setting = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                headers=header,
                json=data,
            )
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/porn",
                headers=header,
            )

        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def gambling(active, config, header):
        if bool:
            data = {"id": "gambling", "active": active}
            setting = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                headers=header,
                json=data,
            )
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/gambling",
                headers=header,
            )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def dating(active, config, header):
        if bool:
            data = {"id": "dating", "active": active}
            setting = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                headers=header,
                json=data,
            )
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/dating",
                headers=header,
            )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def piracy(active, config, header):
        if bool:
            data = {"id": "piracy", "active": active}
            setting = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                headers=header,
                json=data,
            )
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/piracy",
                headers=header,
            )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def socialnetworks(active, config, header):
        if bool:
            data = {"id": "social-networks", "active": active}
            setting = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories",
                headers=header,
                json=data,
            )
        else:
            setting = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/categories/social-networks",
                headers=header,
            )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def safesearch(safeSearch, config, header):
        setting = {"safeSearch": safeSearch}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/parentalcontrol",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def youtubeRestrictedMode(youtubeRestrictedMode, config, header):
        setting = {"youtubeRestrictedMode": youtubeRestrictedMode}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/parentalcontrol",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def blockbypass(blockBypass, config, header):
        setting = {"blockBypass": blockBypass}
        setting = requests.patch(
            f"https://api.nextdns.io/profiles/{config}/parentalcontrol",
            headers=header,
            json=setting,
        )
        if setting.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return setting.text

    @staticmethod
    def blocksite(site, config, header):
        if site in blocksites:
            data = {"id": site, "active": True}
            put = requests.post(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/services/",
                headers=header,
                json=data,
            )
            if put.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", blocksites)
            return f"{site} is no valid parameter!"

    @staticmethod
    def unblocksite(site, config, header):
        if site in blocksites:
            delete = requests.delete(
                f"https://api.nextdns.io/profiles/{config}/parentalcontrol/services/{site}",
                headers=header,
            )
            if delete.text.__contains__("notFound"):
                raise ConfigNotFound(config)
            else:
                return "OK"
        else:
            print("Allowed: ", blocksites)
            return f"{site} is no valid parameter!"


class denylist:
    @staticmethod
    def list(config, header):
        response = requests.get(
            f"https://api.nextdns.io/profiles/{config}/denylist", headers=header
        )
        if response.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        response = response.json()
        return response

    @staticmethod
    def blockdomain(domain, config, header):
        data = {"id": domain, "active": True}
        put = requests.post(
            f"https://api.nextdns.io/profiles/{config}/denylist/",
            headers=header,
            json=data,
        )
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    @staticmethod
    def unblockdomain(domain, config, header):
        delete = requests.delete(
            f"https://api.nextdns.io/profiles/{config}/denylist/{domain}",
            headers=header,
        )
        if delete.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return delete.text


class allowlist:
    @staticmethod
    # TODO: Change the method name from `list` to something different
    def list(config, header):
        settings = requests.get(
            f"https://api.nextdns.io/profiles/{config}/allowlist", headers=header
        )
        if settings.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return settings.json()

    @staticmethod
    def add(domain, config, header):
        data = {"id": domain, "active": True}
        put = requests.post(
            f"https://api.nextdns.io/profiles/{config}/allowlist/",
            headers=header,
            json=data,
        )
        if put.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return put.text

    @staticmethod
    def remove(domain, config, header):
        delete = requests.delete(
            f"https://api.nextdns.io/profiles/{config}/allowlist/{domain}",
            headers=header,
        )
        if delete.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return delete.text


class analytics:
    @staticmethod
    def counter(config, header):
        count = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/status", headers=header
        )
        if count.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        count = count.json()
        return count

    @staticmethod
    def topresolveddomains(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=default",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def topblockeddomains(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=blocked",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def topalloweddomains(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/domains?status=allowed",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def topdevices(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/devices",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def topclientips(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/ips", headers=header
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def toprootdomains(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/domains?root=true",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top

    @staticmethod
    def gafam(config, header):
        gafam = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/destinations?type=gafam",
            headers=header,
        )
        if gafam.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        else:
            return gafam.json()

    @staticmethod
    def trafficdest(config, header):
        top = requests.get(
            f"https://api.nextdns.io/profiles/{config}/analytics/destinations?type=countries",
            headers=header,
        )
        if top.text.__contains__("notFound"):
            raise ConfigNotFound(config)
        top = top.json()
        return top
