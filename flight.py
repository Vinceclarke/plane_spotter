from urllib2 import urlopen
import json
import time
import math
import requests
import re

url1='http://yourIPaddress:8080/data.json'

try:
 x=[]
 y=[]
 distance=[]
 
 #get list of planes seen from your radar
 flight=urlopen(url1).read()
 flight=flight.decode('utf-8')
 results=json.loads(flight)
 
 #get coordinates of all the planes and store them in a lists of tuples
 for i in results:
  lat = i.get("lat")
  lon = i.get("lon")
  x.append(lat)
  y.append(lon)
 z = zip(x,y)
 me=(51.184708,0.268231) #use your coordinates here
 
 #calculate linear distances between you and each plane and store them in a list
 for j in z:
  dist=math.hypot(abs(j[0] - me[0]), abs(j[1] - me[1])) # Linear distance 
  distance.append(dist)
 
 #get the index of the plane closer to you and print its coordinates
 index_min = min(xrange(len(distance)), key=distance.__getitem__)
 closer = z[index_min]
 x0=closer[0]
 x1=closer[1]
 x0=str(x0)
 x1=str(x1)
 print x0, x1
 
 #get the details of 'your plane'from public-api.adsbexchange.com 
 #it could be more precise using the icao of the plane instead of the coordinates
 #for more details look here http://www.virtualradarserver.co.uk/Documentation/Formats/AircraftList.aspx#response 
 try:
  url2="https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat="+ x0 + "&lng=" + x1 + "&fDstL=0&fDstU=5"
  data = requests.get(url2).json()
  
  if not data['acList']:
   print 'There are no planes nearby, try later'
   exit()
  
  if 'acList' in data:
   data1= data['acList'][0]
  
  if 'Call' in data1 and 'Mdl' in data1:
   call= data1['Call']
   model=data1['Mdl']
  
  if 'From' in data1:
   print 'From: ' + data1['From']
  if 'To' in data1:
   print 'To: ' + data1['To']
  
 except IOError:
  print 'error'
except IOError:
 print 'not available'
