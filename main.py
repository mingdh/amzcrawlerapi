from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import requests
import orjson
import config
import plugin
from log import Logger
from os import path

#app = FastAPI()
app = FastAPI(docs_url="/mingdocs", redoc_url=None)

"""
@app.get("/",response_class=ORJSONResponse)
async def read_root():
    return {"Hello": "World"}
"""

logger = Logger(filename=config.logfilename, when='D',backCount=config.backCount,fmt='[%(asctime)s %(name)s] %(levelname)s: %(message)s')
plugin.load_plugins(
        path.join(path.dirname(__file__), 'awesome'),
        'awesome'
    )

@app.get("/",response_class=ORJSONResponse)
async def read(asin: str, c: str = None):

    header = await config.getrandHeader()
    proxy = await config.getrandProxy()
    country = config.getMarketplace(c)

    url = country.format(asin)
    logger.info(orjson.dumps({"url": url, "header": header.get("User-Agent"), "proxy": proxy}))

    #response = requests.get(url,headers=header,proxies={"http": "http://"+ proxy, "https": "https://" + proxy})
    module = plugin.get_loaded_plugins().get(c.lower(), None)
    status = 'fail'
    data = ''
    if module:
        try:
            data = getattr(module,"scrape")(url, header, proxy, logger, path.join(path.dirname(__file__), f'awesome/{c.lower()}.yml'))
        except Exception as err:
            logger.error(f'Failed to run scrape "{url}", error: {err}')
            logger.exception(err)
        else:
            status = 'success'
    logger.info(orjson.dumps({"status": status, "data": data}))

    return {"status": status, "data": data}
    