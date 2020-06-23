import random
import json
import asyncio
from dataobjects import orm, proxys,headers
from utilities import getutcnow

import requests
import random 
from collections import OrderedDict


logfilename = './logs/all.log'
loglevel = "info"
backCount = 5

#default database
dbparams = {'host': '127.0.0.1',
            'port': 3306,
            'user': 'fakeagent',
            'password': 'XbAVlF',
            'db': 'fakeagent',
            'charset': 'utf8',
            'autocommit': True,
            'maxsize': 30,
            'minsize': 5,
}

#common function
async def getrandHeader():

    ret = None
    await orm.create_pool(**dbparams)
    rows = await headers.findAll()
    if rows:
        myheader = json.loads(random.choice(rows).header)
        h = OrderedDict()
        for header,value in myheader.items():
            h[header]=value
        ret = h
    return ret

async def getrandProxy():

    ret = None
    await orm.create_pool(**dbparams)
    rows = await proxys.findAll()
    proxylist = []
    for row in rows:
        h = {}
        if row.enable == 'enable':
            h[row.id] = ':'.join([row.ip,row.port])
            proxylist.append(h)
    if proxylist:
        h = random.choice(proxylist)
        for key,value in h.items():
            id = key
            ret = value
    if ret:
        sql = 'UPDATE `proxys` SET `lastused` = ? WHERE id = ?'
        await orm.execute(sql, [f'{getutcnow()}',id])

    return ret

def getMarketplace(country: str = None):
    with open('config.json') as config_file:
        data = json.load(config_file)
    ret = data.get('marketplace').get('de')
    if country:
        ret = data.get('marketplace').get(country.lower(), ret)
    return  ret