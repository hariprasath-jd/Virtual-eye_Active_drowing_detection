import cv2
import os
import numpy as np
from .utils import downlode_file
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time
from playsound import playsound
import requests
from flask import Flask,request, render_template, redirect, url_for
from cloudant.client import cloudant

client = cloudant.iam()
my_database=client.create_database('my_database')
@app.route('/')
def index():
    return render_template('intex.html')
@app.route('/afterreg' , methods=['post'])
def afterreg():
    x = [x for x in request.form.values()]
    print(x)
    data = {
        '_id':x[1],
        'name':x[0],
        'psw':x[2]
    }
    print(data)
    query = {'_id':{'$eq': data['_id']}}
    docs = my_database.get_query_result(query)
    print(docs)
    print(len(docs.all()))
    if(len(docs.all())==0):
        url = my_database.create_document(data)
        return render_template('register.html', pred="Registration successful, please login using your details")
    else:
        return render_template('register.html', pred="you are already a member, please login using your datails")
    #login page
    @app.route('/login')
    def login():
        return render_template('login.html')
    @app.route('/login')
    def login():
        return render_template('login.html')
    @app.route('/afterlogin',methods=['post'])
    def afterlogin():
        user = request.form['_id']
        passw = request.form['paw']
        print(user,passw)
        query = {'_id':{'$eq':user}}
        docs = my_database.get_query_result(query)
        print(docs)
        print(len(docs.all()))
        if(len(docs.all())==0):
            return render_template('login.html', pred="The username is not found.")
        else:
            if((user==docs[0][0]['_id'] and passw==docs[0][0]['psw'] )):
                return redirect(url_for('prediction'))
            else:
                print('Invalid user')
        @app.route('/Logout')

        def logout():
            return render_template('logout.html')
        @app.route('/result',methods=["GET","post"])
        def res():
          webcam = cv2.VideoCapture('drowning.mp4')

          if not webcam.ioOpened():
            print("could not open webcam")
            exit()

          t0 = time.time()
          center0 = np.zeros(2)
          isDrowning = False
          while webcam.iosOpened():
              status, frame = webcam.read()

          bbox, label ,conf =cv.detect_common_objects(frame)
          if(len(bbox)>0):
              bbox0 = bbox[0]
              center = [0,0]
              center = [(bbox[0]+bbox0[2])/2,(bbox[1]+bbox[3])/2]
              hmov = abs(centre[0]-centre0[0])
              vmov = abs(centre[1]-centre0[1])

              x=time.time()

              threshold = 10
              if(hmov>threshold or vmov>threshold):
                  print(x-t0, 's')
                  t0 = time.time()
                  isDrowning = True
              else:

                  print('bbox: ',bbox, 'centre:', centre, 'centre0:', centre0)
                  print('Is he drawning: ',isDrowning)

                  centre0 = centre
                  out = draw_bbox(frame, bbox, label, conf, isDrowning)

                  cv2.imshow("Real-time object detection", out)
                  if(isDrowning == True):
                      playsound('alarm.mp3')
                      webcam.release()

                      cv2.imshow("Real-time object detection", out)
                      if(isDrowning == True):
                          playsound('alarm.mp3')
                          webcam.release()
                          cv2.destroyAllwindows()
                          return render_template('pradiction.html', prediction = "Emergency !!! The person is drowining")

                      if cv2.waitkey(1) & 0xFF == ord('q'):
                          break

                          webcam.release()
                          cv2.destroyAllwindows()
          """Running our application"""
                      if _name_ -- "_main_":
                         app.run(debug=True)