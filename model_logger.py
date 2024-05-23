import requests,time,threading

mainwebhook =""
decalwebhook = ""
autodownloadwebhook = ""
whitelist = [5845922908,1395153130,3497178500] #5845922908 forever  1395153130 03.05.24
errors404counter = 0
modelcount = 99
speedcheck = True
lastid = 17566476240-modelcount
threadscount = 3
countofworktime = 15
avarageworktime = []
modelsids = []


coloredtext ={"True":"""
```ansi
[2;32m[0m[2;35m[0m[2;32mTrue[0m
```""",
"False":"""
```ansi
[2;32m[0m[2;35m[0m[2;32m[2;31mFalse[0m[2;32m[0m
```
"""
}
def checkasstid(id,embed):
 if speedcheck:
     return
 id = int(id)
 try:
  r = requests.get("https://assetdelivery.roblox.com/v1/asset/?id="+str(id))
 except:
  checkasstid(id,embed)
  return

 try:
   r.json()
   return
 except: None
 content = str(r.content).lower()
 tags = ""
 shoulddownload = 0
 hasscript = "False"
 if content.find("linkedsource") != -1 or content.find("modulescript") != -1 or content.find("scriptguid") != -1:
     hasscript = "True"
 if content.find("async") != -1:
     tags = "HttpService functions(Possible) "
     shoulddownload+=2.5
 if content.find("httpservice") != -1:
     tags = tags+"HttpService(Verified) "
     shoulddownload +=1.5
 if content.find("webhooks") != -1 or content.find("webhook") != -1:
     tags = tags+"Webhook "
     shoulddownload += 3
 if content.find("postasync") != -1:
     tags = tags+"PostAsync "
     shoulddownload+= 1.5
 if content.find("getasync") != -1:
     tags = tags+"GetAsync "
     shoulddownload+=1.5  
 if content.find("requestasync") != -1:
     tags = tags+"RequestAsync "
     shoulddownload+=1.5 
 if content.find("bit32") != -1 or content.find("bxorf") != -1  or content.find("ldexp") != -1  or content.find("byte") != -1:
     tags = tags+"Obfuscation(Possible) " 
     shoulddownload+=0.5 
 if shoulddownload >= 3:
    open(str(id)+".rbxm","wb").write(r.content) 
    requests.post(autodownloadwebhook,json={"content":None,
                                            "embeds":[{"description":str(id),
                                                       "color":None,
                                                       "fields":[{"name":"Reasons:"+str(shoulddownload),
                                                                  "value":tags}],
                                                                  "author":{"name":"Model Downloaded!"}}],
                                                                  "attachments":[]})
 if tags != "":
    embed["embeds"][0]["fields"].append({"name":"Detected","value":tags})   
 if hasscript == "True":
    embed["embeds"][0]["fields"].append({"name":"hasScripts","value":coloredtext[hasscript]})  
 requests.post(mainwebhook,json=embed)
cached_sessions = {}
friendaccountrequests = []


url = "https://apis.roblox.com/toolbox-service/v1/items/details?assetIds="
iconurl = "https://thumbnails.roblox.com/v1/assets?assetIds="


def gettumbnale(assetid:int,wait):
    if wait:
        time.sleep(20)
    a = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={str(assetid)}&returnPolicy=PlaceHolder&size=250x250&format=png").json()
    #print(a)
    return a["data"][0]["imageUrl"]
def getuserinfo(userid:int):
    a = requests.get(f"https://users.roblox.com/v1/users/{str(userid)}").json()
    return a

def senddecallog(v,v1):
            thumbnale = gettumbnale(v["id"],True)
            user = {"name":v1["creator"]["name"],"id":str(v1["creator"]["id"])}
            modelsids.append(v["id"])

            embed = {"embeds":
                [
                {"title":v["name"],
                "description":v["description"],
                "url":"https://create.roblox.com/store/asset/"+str(v["id"]),
                "color":16743658,
                "fields":[
                    {"name":"createdUtc","value":v["createdUtc"]},
                    {"name":"Creator","value":user["name"]+f" ("+user["id"]+"}"}
                    ],
                    "author":{"name":"Asset id: "+str(v["id"])},
                    "thumbnail":{"url":thumbnale}}
                    ]
                    ,"attachments":[]}
            requests.post(decalwebhook,json=embed)
def sendmodellog(v,v1):
    if v1["creator"]["id"] in whitelist:
        return
    thumbnale = gettumbnale(v["id"],False)            
    user = {"name":v1["creator"]["name"],"id":str(v1["creator"]["id"])}
    modelsids.append(v["id"])

    embed = {"embeds":
        [
        {"title":v["name"],
        "description":v["description"],
        "url":"https://create.roblox.com/store/asset/"+str(v["id"]),
        "color":16743658,
        "fields":[
            #{"name":"isForSale","value":coloredtext[str(v1["product"]["isForSaleOrIsPublicDomain"])]},
            {"name":"createdUtc","value":v["createdUtc"]},
            {"name":"Creator","value":user["name"]+f" ("+user["id"]+"}"}
            ],
            "author":{"name":"Asset id: "+str(v["id"])},
            "thumbnail":{"url":thumbnale}}
            ]
            ,"attachments":[]}
    #requests.post(mainwebhook,json=embed)
    checkasstid(v["id"],embed)
def checkids(id):
    global errors404counter
    #time.sleep(.2)
    ids = []
    i2 = -1
    for i in range(1,modelcount+1):
        ids.append(str(id+i))
    ids = "%2C".join(ids)

    result = None
    try:
        result = requests.get(url+ids).json()
    except:
        checkids(id)
        return
    if not "data" in result:
        
        #print("Nothing founded status "+str(result["status"]))
        if result["status"] != 403 and result["status"] != 404:
            print(result)
            checkids(id)
            return
        elif result["status"] == 404:
            errors404counter += 1
    elif "data" in result:
        errors404counter = 0
        for v in result["data"]:
            i2 += 1
            v1 = v
            v = v["asset"]
            #iconv = result2[i]["imageUrl"]
            
          
            if (v["typeId"] != 10 and v["typeId"] != 13) or v["id"] in modelsids:
                continue
            
            if v["typeId"] == 13:
                threading.Thread(target=senddecallog,args=(v,v1)).start()
                #senddecallog(v,v1)
            elif v["typeId"] == 10:
                threading.Thread(target=sendmodellog,args=(v,v1)).start()
                
                
print("Starting loop")


speedcheck = False
while True:
    if errors404counter >= 100:
        lastid= lastid-(modelcount*errors404counter)*2
        print("Too much 404 cooldown on few seconds")
        time.sleep(5)
        errors404counter = 0  
        
    time.sleep(.35/3)
    lastid = lastid+modelcount
    
    threading.Thread(target=checkids,args=(lastid,),daemon=True).start()
   
    print(lastid)
    if modelsids.__len__() >= 200:
        #print("Clearing old assets")
        del modelsids[0]
        