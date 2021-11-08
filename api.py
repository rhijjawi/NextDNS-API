import requests
import json

nativetracking = ["sonos", "xiaomi", "apple", "windows", "huawei", "samsung", "alexa", "roku"]
nativetrackinghex = ["736f6e6f73","7869616f6d69","6170706c65","77696e646f7773","687561776569","73616d73756e67","616c657861","726f6b75"]
siteshex = {
"tiktok":"74696b746f6b",
"tinder":"74696e646572",
"facebook":"66616365626f6f6b",
"snapchat":"736e617063686174",
"instagram":"696e7374616772616d",
"fortnite":"6570696367616d65732f666f72746e6974652f686f6d65",
"messenger":"6d657373656e676572",
"leagueoflegends":"6c65616775656f666c6567656e6473",
"9gag":"39676167",
"tumblr":"74756d626c72",
"vk":"766b",
"roblox":"726f626c6f78",
"twitch":"747769746368",
"minecraft":"6d696e656372616674",
"pinterest":"70696e746572657374",
"discord":"646973636f7264617070",
"twitter":"74776974746572",
"dailymotion":"6461696c796d6f74696f6e",
"whatsapp":"7768617473617070",
"steam":"737465616d",
"youtube":"796f7574756265",
"hulu":"68756c75",
"reddit":"726564646974",
"blizzard":"626c697a7a617264",
"netflix":"6e6574666c6978",
"imgur":"696d677572",
"vimeo":"76696d656f",
"disney+":"6469736e6579706c7573",
"telegram":"74656c656772616d",
"skype":"736b797065",
"ebay":"65626179",
"spotify":"73706f74696679",
"amazon":"616d617a6f6e",
"zoom":"7a6f6f6d",
"primevideo":"7072696d65766964656f"}

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
    def login(email:str=None, password:str=None, otp:str=None):
        if (email == None or password == None) or (email == None and password == None):
            raise NoCredentials 
        else:
            success = False
            json = {"email":f"{email}","password":f"{password}"}
            while success == False:
                login = requests.post('https://api.nextdns.io/accounts/@login', headers=headers, json=json)
                if login.text == "OK":
                    success = 1
                elif login.text == """{"requiresCode":true}""":
                    code = otp or input("""Please enter 2FA Code: """)
                    json = {"email":f"{email}","password":f"{password}","code":f"{code}"}
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

class settings:
    def listsettings(config,header):
        list = requests.get(f"https://api.nextdns.io/configurations/{config}/settings", headers=header)
        if list.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            list = list.json()
            return list
    def setup(config,header):
        setup = requests.get(f"https://api.nextdns.io/configurations/{config}/setup", headers=header)
        if setup.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            setup = setup.json()
            return setup
    def clearlogs(config,header):
        logs = requests.delete(f"https://api.nextdns.io/configurations/{config}/logs", headers = header)
        if logs.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return logs.text
    def rename(name, config, header):
        nname = {"name":name}
        rename = requests.patch(f"https://api.nextdns.io/configurations/{config}/settings", headers = header, json=nname)
        if rename.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return f"Config renamed to {name}"
    def delete(config,header):
        dconfig = requests.delete(f"https://api.nextdns.io/configurations/{config}", headers = header)
        if dconfig.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return f"Config {config} deleted"
    def logclientips(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        logcips = {"logging_disable_client":bool}
        logcips = requests.patch(f"https://api.nextdns.io/configurations/{config}/settings", headers = header, json=logcips)
        if logcips.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return logcips.text
    def logdomains(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        logdom = {"logging_disable_query":bool}
        logdom = requests.patch(f"https://api.nextdns.io/configurations/{config}/settings", headers = header, json=logdom)
        if logdom.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return logdom.text
    def blockpage(bool,config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        bp = {"blockPage":bool}
        bp = requests.patch(f"https://api.nextdns.io/configurations/{config}/settings", headers = header, json=bp)
        if bp.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return bp.text
    def updatelinkedip(config,header):
        r = settings.setup(config, header)
        updatetoken = r["linkedIpUpdateToken"]
        updateip = requests.get(f"https://link-ip.nextdns.io/{config}/{updatetoken}")
        if updateip.text != "Bad Request":
            raise ConfigNotFound(config)
        else:
            return updateip.text

class security:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/configurations/{config}/security", headers = header)
        if settings.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings
    def threatintelligencefeeds(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"threatIntelligenceFeeds":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def aidetection(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"aiThreatDetection":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def safebrowsing(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"googleSafeBrowsing":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def cryptojacking(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"cryptojacking":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def dnsrebinding(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"dnsRebinding":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def homograph(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"homograph":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def typosquatting(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"typosquatting":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def dga(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"dga":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def newdomains(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"nrd":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def parked(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"parked":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def csam(bool, config, header): 
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"csam":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/security", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def addtld(tld, config, header):
        hex = tld.encode('utf-8').hex()
        hex = f"hex:{hex}"
        put = requests.put(f"https://api.nextdns.io/configurations/{config}/security/blocked_tlds/{tld}", headers = header)
        if put.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return put.text
    def removetld(tld, config, header):
        hex = tld.encode('utf-8').hex()
        hex = f"hex:{hex}"
        remove = requests.delete(f"https://api.nextdns.io/configurations/{config}/security/blocked_tlds/{tld}", headers = header)
        if remove.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return remove.text

class privacy:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/configurations/{config}/privacy", headers = header)
        if settings.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings
    def blockdisguised(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"blockDisguised":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/privacy", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def blockaffiliate(bool, config, header):
        if bool == True:
            bool = "false"
        else:
            bool = "true"
        setting = {"allowAffiliate":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/privacy", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def blocknative(native, config, header):
        hex = native.encode('utf-8').lower().hex()
        
        if hex in nativetrackinghex:
            hex = f"hex:{hex}"
            put = requests.put(f"https://api.nextdns.io/configurations/{config}/privacy/natives/{hex}", headers = header)
            if put.text == "Not Found":
                raise ConfigNotFound(config)
            else:
                return "OK"
    def unblocknative(native, config, header):
        hex = native.encode('utf-8').lower().hex()
        
        if hex in nativetrackinghex:
            hex = f"hex:{hex}"
            delete = requests.delete(f"https://api.nextdns.io/configurations/{config}/privacy/natives/{hex}", headers = header)
            if delete.text == "Not Found":
                raise ConfigNotFound(config)
            else:
                return "OK"

class parental:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/configurations/{config}/parentalcontrol", headers = header)
        if settings.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            settings = settings.json()
            return settings
    def porn(bool, config, header):
        if bool == True:
            setting = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:706f726e", headers = header)
        else:
            setting = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:706f726e", headers = header)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def gambling(bool, config, header):
        if bool == True:
            setting = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:67616d626c696e67", headers = header)
        else:
            setting = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:67616d626c696e67", headers = header)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def dating(bool, config, header):
        if bool == True:
            setting = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:646174696e67", headers = header)
        else:
            setting = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:646174696e67", headers = header)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def piracy(bool, config, header):
        if bool == True:
            setting = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:706972616379", headers = header)
        else:
            setting = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:706972616379", headers = header)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def socialnetworks(bool, config, header):
        if bool == True:
            setting = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:736f6369616c2d6e6574776f726b73", headers = header)
        else:
            setting = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/categories/hex:736f6369616c2d6e6574776f726b73", headers = header)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def safesearch(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"safeSearch":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/parentalcontrol", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return settings
    def youtubeRestrictedMode(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"youtubeRestrictedMode":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/parentalcontrol", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def blockbypass(bool, config, header):
        if bool == True:
            bool = "true"
        else:
            bool = "false"
        setting = {"blockBypass":bool}
        setting = requests.patch(f"https://api.nextdns.io/configurations/{config}/parentalcontrol", headers = header, json=setting)
        if setting.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return setting.text
    def blocksite(site, config, header):
        try:
            sitehex = siteshex[f"{site.lower()}"]
        except:
            raise OptionUnavailable(allowed=site)
        put = requests.put(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/services/hex:{sitehex}", headers = header)
        if put.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return put.text
    def unblocksite(site, config, header):
        sitehex = siteshex[f"{site.lower()}"]
        delete = requests.delete(f"https://api.nextdns.io/configurations/{config}/parentalcontrol/services/hex:{sitehex}", headers = header)
        if delete.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return delete.text

class denylist:
    def list(config, header):
        list = requests.get(f"https://api.nextdns.io/configurations/{config}/denylist", headers=header)
        if list.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            list = list.json()
            return list
    def blockdomain(domain, config, header):
        hex = domain.encode('utf-8').hex()
        put = requests.put(f"https://api.nextdns.io/configurations/{config}/denylist/hex:{hex}", headers = header)
        if put.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return put.json()
    def unblockdomain(domain, config, header):
        hex = domain.encode('utf-8').hex()
        delete = requests.delete(f"https://api.nextdns.io/configurations/{config}/denylist/hex:{hex}", headers = header)
        if delete.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return delete.json()

class allowlist:
    def list(config, header):
        settings = requests.get(f"https://api.nextdns.io/configurations/{config}/allowlist", headers = header)
        if settings.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return settings.json()
    def add(domain, config, header):
        hex = domain.encode('utf-8').hex()
        put = requests.put(f"https://api.nextdns.io/configurations/{config}/allowlist/hex:{hex}", headers = header)
        if put.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return put.json()
    def remove(domain, config, header):
        hex = domain.encode('utf-8').hex()
        delete = requests.delete(f"https://api.nextdns.io/configurations/{config}/allowlist/hex:{hex}", headers = header)
        if delete.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            return delete.json()

class analytics:
    def counter(config, header):
        count = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/counters", headers = header)
        if count.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            count = count.json()
            return count
    def topresolveddomains(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_domains/resolved", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def topblockeddomains(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_domains/blocked", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def toplists(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_lists", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def topdevices(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_devices", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def topclientips(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_client_ips", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def toprootdomains(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/top_root_domains", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
    def gafam(config, header):
        gafam = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/gafam", headers = header)
        if gafam.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = gafam.json()
            return top
    def trafficdest(config, header):
        top = requests.get(f"https://api.nextdns.io/configurations/{config}/analytics/traffic_destination_countries", headers = header)
        if top.text == "Not Found":
            raise ConfigNotFound(config)
        else:
            top = top.json()
            return top
