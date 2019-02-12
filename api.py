import requests
import re
import json
import os

def http_get(request,payload):
    r =requests.get(request,params=payload)
    return r

def get_api(payload):
    page_url = "https://escapefromtarkov.gamepedia.com/api.php"
    return http_get(page_url,payload)

def get_page(page,prop,additionalPayload = {}):
    payload = {'action':'parse','page':page,'format':'json','prop':prop,**additionalPayload}

    return get_api(payload)

def serialize(filename,data):
    data = json.dumps(data)
    with open(filename,'w') as f:
        f.write(data)

def deserialize(filename):
    with open(filename,'r') as f:
        return json.load(f)

def cache_dir():
    return os.path.join('.','__cache__')

def assert_cache_folder_exists():
    if os.path.isdir(cache_dir()):
        return
    os.mkdir(cache_dir())

def cached(file,fn):
    p = os.path.join(cache_dir(),file)
    assert_cache_folder_exists()
    if os.path.isfile(p):
        return deserialize(p)

    data = fn()
    serialize(p,data)
    return data

def get_ammo_info():
    ammopage = get_page("Ammunition",'links').json()['parse']['links']
    infobox_regex = re.compile("\{\{Infobox ammo(.*)\}\}",re.DOTALL)
    dataname_regex = re.compile('\|[a-z]+\s*=')
    data_regex = re.compile('=(.*)$')

    ammos = []
    for maybeAmmo in ammopage:
        maybeAmmoName = maybeAmmo['*']
        categories = get_page(maybeAmmoName,'categories')
        categoryNames = list(map(lambda x:x['*'],categories.json()['parse']['categories']))
        
        if 'Ammo' in categoryNames:
            templateName = 'Template:Infobox ammo'
            content = get_page(maybeAmmoName,'wikitext').json()['parse']['wikitext']['*']
            infobox = infobox_regex.findall(content)[0].split("\n")
            valueDict = {}
            for infobox_line in infobox:
               
                datatypeNames = dataname_regex.findall(infobox_line)
                datas = data_regex.findall(infobox_line)
                if  len(datatypeNames) == 1 and len(datas) == 1:
                    datatypeName = datatypeNames[0].replace('|','').replace('=','').strip()
                    data = datas[0].replace('=','').strip()
                    
                    valueDict[datatypeName]= data
            valueDict['category'] = categoryNames[0]
            valueDict['name']=maybeAmmoName
            ammos.append(valueDict)
    traderslevels = set()
    for ammo in ammos:
           traderstring = ammo['trader']
           traders = traderstring.split('<br/>')
           for t in traders:
               traderslevels.add(t)
    print('Traders:',traderslevels)
    traderslevels = list(traderslevels)
    for ammo in ammos:
           traderstring = ammo['trader']
           traders = traderstring.split('<br/>')
           for trader in traderslevels:
               ammo['Trader:' +trader] = trader in traders

    return ammos
   
def find_common_start(list_of_strings):
    list_of_strings = list(set(list_of_strings))
    if len(list_of_strings== 0):
        return []
    abort = False
    commonstring = ""
