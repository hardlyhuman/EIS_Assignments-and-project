import requests
import urllib
import traceback
import re
while 1:
    s=""
    l=""
    try:
        v=requests.get('http://192.168.43.134:1336')
        print ("111",v.text)
        print (v.text)
    except :
        s = str(traceback.format_exc())
    print (s)
    if "Bad" in s:
        s=s[s.index("Bad"):]
        s=s[15:]
        try:
            s=s[:s.index('\\r')]
            l=s.split(":")
        except:
            pass
        print ("this is l")
        print (l)
        if l:
            print ("we have: "+urllib.quote(l[0]))
            r=urllib.urlopen("https://energymanagement.pythonanywhere.com/energy_management/default/temp?f1="+urllib.quote(l[0]))
            print (r,"success")
        
    
