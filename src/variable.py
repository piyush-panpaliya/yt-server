# import json
import pickledb
db = pickledb.load('data.db', True)

jsondata = db.get('config')


VIDEO=str(jsondata['VIDEO'])
key=str(jsondata['KEY'])
AUDIO=str(jsondata['AUDIO'])
AD=str(jsondata['AD'])
playAd=jsondata['playAd']
forceUpdateMusic=jsondata['forceUpdateMusic']
adInterval=int(jsondata['adInterval'])
totalsongs=int(jsondata['totalsongs'])
command=str(jsondata['command'])+key
BackupCommand=str(jsondata['backupCommand'])+key

current=1
downloading=False
