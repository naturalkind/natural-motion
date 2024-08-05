import __init__
import os, sys, glob, time, json, io

import cv2
import numpy as np
import glob, uuid, base64, json, time
import subprocess
# филтр калмана
from nn.KalmanFilter import *
# позы
from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose
# селдерей
from celery import Celery
from celery.utils.log import get_task_logger
from celery.signals import worker_init, worker_process_init
from celery.concurrency import asynpool

logger = get_task_logger(__name__)

CELERY_BROKER_URL = 'redis://localhost:6379/'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/'

# Celery: Distributed Task Queue
app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
app.conf.task_serializer   = 'json'
app.conf.result_serializer = 'json'

SESSION_PATH = './nn/Lifting-from-the-Deep-release-master/data/saved_sessions/init_session/init'
PROB_MODEL_PATH = './nn/Lifting-from-the-Deep-release-master/data/saved_sessions/prob_model/prob_model_params.mat'

global_bone_dict = {'base': 0, 'pelvis_r': 0, 'thigh_r': 0, 'calf_r': 0, 'pelvis_l': 0, 
                    'thigh_l': 0, 'calf_l': 0, 'waist': 0, 'chest': 0, 
                    'neck': 0, 'head': 0, 'shoulder_l': 0, 'arm_l': 0, 
                    'forearm_l': 0, 'shoulder_r': 0, 'arm_r': 0, 'forearm_r': 0}

list_bone_key_dict = list(global_bone_dict.keys())  

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Папка '{folder_path}' создана.")
[create_folder(z) for z in ["data", "videos", "file"]]

@app.task(name='func_celery')
def func_celery(video_file):
    print (video_file)
    cap = cv2.VideoCapture(video_file)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print ((w,h,3))
    pose_estimator = PoseEstimator((h,w,3), SESSION_PATH, PROB_MODEL_PATH)
    pose_estimator.initialise()
    outfile = open(f'data/{video_file.split("/")[-1].split(".")[0]}_data_kalman.txt', 'w')
    idx = 0
    while True:
        ret, image = cap.read()
#        if idx == 90:
#            print ("90 idx FINAL........................")
#            break
        if ret == False:
            break
        try:    
            pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
            for ii in pose_3d:
                coordinates = []
                for i in range(len(ii[0])):
                    # фильтр калмана
                    out_kalman_x, out_kalman_y, out_kalman_z = kalman_process.do_kalman_filter(ii[0][i], ii[1][i], ii[2][i], list_bone_key_dict[i])
                    coordinates.append([out_kalman_x, out_kalman_y, out_kalman_z])                
                outfile.write(str(json.dumps(coordinates))+"\n")  
            idx+=1
        except Exception as e:
            print ("ERROR:", e)
    outfile.close()
    cap.release()
    cv2.destroyAllWindows()
    
    # запуск blender
    blender_start = subprocess.call(f'blender --background --python blender_app.py -- asss {video_file.split("/")[-1].split(".")[0]}', shell=True)
    print (blender_start)       

