import cloudinary
import cloudinary.uploader
from flask import Flask
from flask import request, redirect
import json
import requests
import cv2
import os
import numpy
from PIL import Image
from flask import Response,jsonify,make_response
app = Flask(__name__)

@app.route('/api/upload/cloudinary', methods=['POST'])
def upload():
    #email = request.form['email']
    f = request.files['image']
    print(f)
    cloudinary.config(cloud_name="shubhambhattacharya",api_key="442859552564425",api_secret="NAhJuoBcjjfP886c0n2xwvR7jPI")
    d = cloudinary.uploader.upload(f)
    print (d)
    return json.dumps(d)
@app.route('/')
def home():
        return 'shubham'

@app.route('/ocr',methods=['POST'])
def ocr():
    payload = {'url':'','isOverlayRequired': True,'apikey': 'a4924b356c88957','language': 'eng'}
    r = requests.post('https://api.ocr.space/parse/image',data=payload)
    print (r.content.decode())
    return "shubham"
@app.route('/api/upload', methods=['POST'])
def uploadText():
    #email = request.form['email']
    gKey = 'AIzaSyDExPzZhp40AhE3mQOXXSeDI5fd_Dto_9g'
    f = request.files['image']
    image = cv2.imdecode(numpy.fromstring(request.files['image'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray,[int(cv2.IMWRITE_JPEG_QUALITY), 20])
    print(filename)
    cloudinary.config(cloud_name="shubhambhattacharya",api_key="442859552564425",api_secret="NAhJuoBcjjfP886c0n2xwvR7jPI")
    d = cloudinary.uploader.upload(filename)
    #os.remove(filename)
    print(d['secure_url'])
    payload = {'url':d['secure_url'],'isOverlayRequired': True,'apikey': 'a4924b356c88957','language': 'eng'}
    r = requests.post('https://api.ocr.space/parse/image',data=payload)
    #print (r.json())
    resp = r.json()
    #resp = Response(s, mimetype='application/json')
    #print(resp)
    words = resp['ParsedResults'][0]['TextOverlay']['Lines']
    myWords = []
    for word in words:
        myWords.append(word['Words'][0]['WordText'])
    if(len(myWords) >= 3):
        googleResp = requests.get('https://www.googleapis.com/customsearch/v1?key='+gKey+'&cx=015528857462049392512:iqcemyfrksa&q='+myWords[0]+' '+myWords[1]+' '+myWords[2])
    elif(len(myWords) < 3 and len(myWords) >= 2):
        googleResp = requests.get('https://www.googleapis.com/customsearch/v1?key='+gKey+'&cx=015528857462049392512:iqcemyfrksa&q='+myWords[0]+' '+myWords[1])
    else:
        googleResp = requests.get('https://www.googleapis.com/customsearch/v1?key='+gKey+'&cx=015528857462049392512:iqcemyfrksa&q='+myWords[0])
    #googleResp = googleResp['items']
    google = googleResp.json()
    #print(google)
    items = google['items']
    responseArr = []
    for item in items:
        myObj = {}
        myObj['title'] = item['title']
        myObj['url'] = item['link']
        myObj['description'] = item['snippet']
        responseArr.append(myObj)
    
    return make_response(jsonify(responseArr))
