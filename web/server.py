import __init__
import os, sys, glob, time, json, io
import glob, uuid, base64
import matplotlib.pyplot as plt
import cv2
import numpy as np

from collections import defaultdict

from PIL import Image
from tqdm import tqdm
from moviepy.editor import * 


from tornado.escape import json_encode
from tornado import websocket, web, ioloop
import tornado.ioloop
import tornado.web
import tornado.websocket
import subprocess

#_celery_start_ = subprocess.call(f'celery -A start_celery worker --loglevel=info', shell=True)
#print (_celery_start_)  

from nn.KalmanFilter import *

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose
from start_celery import func_celery 

 
#Получить координаты скилета
def lift_image(value):
    with open(value) as f:
         f = f.readlines()
         ls = []         
         for i in f:
            ls.append(json.loads(i))
         return ls
         
class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()
    myfile = 0
    namefile = 0
    Blist = []
    def check_origin(self, origin):
        return True
    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket opened from: " + self.request.remote_ip)
    def on_message(self, message):
        ms =  json.loads(message)
        print ("message >>>", ms["process"])
        if ms["process"] == "Start":
            self.namefile = f'videos/{ms["Name"]}'
            self.myfile = open(self.namefile, "wb")
            self.write_message(json.dumps({"process":"MoreData"}))
        if ms["process"] == "Upload":
            da = ms["Data"]
            da = da.split(",")[1]
            file_bytes = io.BytesIO(base64.b64decode(da)).read()
            self.myfile.write(file_bytes)
            self.write_message(json.dumps({"process":"MoreData"}))
            
        if ms["process"] == "Done":
            Adata = func_celery.delay(self.namefile)
            self.Blist.append(Adata)
            self.write_message(json.dumps({"process":"progress"}))
        if ms["process"] == "progress":  
            print (self.Blist)
            for ix, i in enumerate(self.Blist):
                if i.status == "SUCCESS":
                    del self.Blist[ix]
#                if i.status == "PENDING":            
                print (i.status)
            if len(self.Blist) == 0:
                self.write_message(json.dumps({"process":"Done", "file": f'{self.namefile.split("/")[-1].split(".")[0]}.bvh'}))
            else:
                self.write_message(json.dumps({"process":"progress"}))
            
    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket closed from: " + self.request.remote_ip)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Нейронная сеть/Тренировка")

if __name__ == '__main__':
    app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/websocket", ImageWebSocket),
            (r"/(three.min.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/three/build/'}),
            (r"/jsm/loaders/(BVHLoader.js)", tornado.web.StaticFileHandler, {'path':'./node_modules/three/examples/jsm/loaders/'}),
            (r"/jsm/controls/(OrbitControls.js)", tornado.web.StaticFileHandler, {'path':"./node_modules/three/examples/jsm/controls/"}),
            (r"/build/(three.module.js)", tornado.web.StaticFileHandler, {'path':"./node_modules/three/build/"}),
            (r"/(main.css)", tornado.web.StaticFileHandler, {'path':"./css/"}),
            (r"/files/(RobotoMono-Regular.woff2)", tornado.web.StaticFileHandler, {'path':"./css/"}),
            (r"/models/bvh/(.*)", tornado.web.StaticFileHandler, {'path':'./file'}),
        ])

    app.listen(8800)
    tornado.ioloop.IOLoop.current().start()
