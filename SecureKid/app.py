import re
import time
from flask import Flask, render_template, request
import reverse_geocoder as rg
import googlemaps
import requests
import json
gmaps = googlemaps.Client(key='AIzaSyCn2LdtM5N7wyYtt9uBE7c0lUiMwl5SQdA')
URL = 'https://www.way2sms.com/api/v1/sendCampaign'
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)
prev=[]
wpTime=0
timeout=30
app = Flask(__name__)

@app.route('/')
def location():
   return render_template('geolocation.html')
   
@app.route('/login',methods=['POST','GET'])
def login():
   lat=request.form['lat']
   lon=request.form['lon']
   coordinates =(lat,lon) 
   result = rg.search(coordinates)
   sp=['ambattur estate','tambaram']
   w=['thirumangalam','koyambedu']
	
   cur=result[0]['name']
   print (cur)
   if len(prev)!=0:
      if(cur!=prev[-1]):
         wpTime=0
         if cur in w:
            wpTime=wpTime+1
         elif cur not in sp:
            response = sendPostRequest(URL, '9YC0M0G1T7MY7UZB2JJDQ7GB49JF2GDL', 'CKAHL8MRLZ7T2AAA', 'stage', '9944375924', 'sowmya08', 'Alert!! your ward is in '+cur+' which is not listed in the safe points you provided.' )
           
      else:
         if cur in w:
            if(wpTime>30):
               response = sendPostRequest(URL, '9YC0M0G1T7MY7UZB2JJDQ7GB49JF2GDL', 'CKAHL8MRLZ7T2AAA', 'stage', '9944375924', 'sowmya08', 'Alert!! your ward is in '+cur+' for an unusually long period.' )
            wpTime=wpTime+1
         if cur == sp[1]:
               response = sendPostRequest(URL, '9YC0M0G1T7MY7UZB2JJDQ7GB49JF2GDL', 'CKAHL8MRLZ7T2AAA', 'stage', '9944375924', 'sowmya08', 'Your ward has reached '+cur)
            
   else:
      if cur in w:
         wpTime=wpTime+1
      elif cur not in sp:
         response = sendPostRequest(URL, '9YC0M0G1T7MY7UZB2JJDQ7GB49JF2GDL', 'CKAHL8MRLZ7T2AAA', 'stage', '9944375924', 'sowmya08', 'Alert!! your ward is in '+cur+' which is not listed in the safe points you provided.' )
      
   time.sleep(timeout)
   print(prev)
	
   prev.append(result[0]['name'])
	
   return render_template("geolocation.html")


if __name__ == '__main__':
   app.run(debug = True)
