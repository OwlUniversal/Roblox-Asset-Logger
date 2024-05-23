# Roblox-Asset-Logger
Can log last models and decal also check script source on https things and on possible backdoors
### Requirements
Make sure you have installed latest python with pip and python is in windows path and you have installed libraries as requests,time,threading
### Setup
Just download and unpack all files in 1 folder <br>
change lastid variable on last toolbox model id you can get it by upload something
```py
lastid = lastidhere-modelcount
```
<br> add your webhook in mainwebhook,decalwebhook,autodownloadwebhook variables 
```py
mainwebhook ="webhookhere"
decalwebhook = "webhookhere"
autodownloadwebhook = "webhookhere"
```
### Notes
you can change time.sleep(.35/3) on more slow if you have bad cpu 
```lua
.35 is speed
3 is thread count
```
### Run
Run cmd in folder with model logger
```sh-session
py model_logger.py
```
