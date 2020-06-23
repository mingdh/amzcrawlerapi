from selectorlib import Extractor
from selectorlib.formatter import Formatter
import requests 
import json, re

class EuroPrice(Formatter):
    def format(self, text):
        price = ''.join(text.split()).replace('€','').strip().replace('.','')
        return price.replace(',','.')

class Images(Formatter):
    def format(self,text):
        ret = []
        if text:
            try:
                picList = json.loads(text)
                for key in picList.keys():
                    ret.append(key)
            except:
                pass
        return ret

class Cates(Formatter):
    def format(self,text):
        ret = set()
        if text:
            pattern = re.compile(r".*?((\d+\.){1,3})*(\d+){1,3}\sin\s(\w+)", re.U)
            groups = pattern.findall(text)
            for p in groups:
                ret.add(p[-1])
            pattern = re.compile(r"\(\sSiehe\sTop\s((\d+\.){0,3})*(\d+){1,3}\sin\s(\w+)", re.U)
            groups = pattern.findall(text)
            for p in groups:
                ret.add(p[-1])
        return list(ret)

class dpAsin(Formatter):
    def format(self,text):
        ret = None
        if text:
            matchObj = re.search(r"(ASIN)(.*?)(\w+)",text,re.U)
            if matchObj:
                ret = matchObj.group(matchObj.lastindex)
        return ret

def scrape(url, headers, proxy, logger, filename):

    try:
        # Create an Extractor by reading from the YAML file
        e = Extractor.from_yaml_file(filename,formatters = [EuroPrice,Images,Cates,dpAsin])
    except Exception as e:
        logger.error(f'Failed to import "{filename}", error: {e}')
        logger.exception(e)
        return None
    
    try:
        r = requests.get(url,headers=headers,proxies={"http": "http://"+ proxy, "https": "https://" + proxy})
    except Exception as e:
        logger.error(f'Failed to requests "{url}", error: {e}')
        logger.exception(e)
        return None

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            logger.info("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            logger.info("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    
    # Pass the HTML of the page and create
    ret = e.extract(r.text)
    for key, value in ret.items():
        if isinstance(value,list):
            newList = []
            for p in value:
                if not (p == None):
                    newList.append(p)
            ret[key] = newList
    return ret
