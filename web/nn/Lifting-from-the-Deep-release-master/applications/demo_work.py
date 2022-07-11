#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Dec 20 17:39 2016

@author: Denis Tome'
"""

import __init__

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose

import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath
import json

DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = PROJECT_PATH + '/data/images/test_image.png'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'


def main():
     cap = cv2.VideoCapture("/media/sadko/1b32d2c7-3fcf-4c94-ad20-4fb130a7a7d4/PLAYGROUND/blender-motion/web/videos/0001-0643.mp4")
     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

     #print ((w,h,3))
     pose_estimator = PoseEstimator((h,w,3), SESSION_PATH, PROB_MODEL_PATH)
     pose_estimator.initialise()
     outfile = open('data_c.txt', 'w')
     while True:
            ret, image = cap.read()
            if ret == False:
                break
            pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
            for ii in pose_3d:
                coordinates = []
                for i in range(len(ii[0])):
                    coordinates.append([ii[0][i], ii[1][i], ii[2][i]])
                outfile.write(str(json.dumps(coordinates))+"\n")  
            draw_limbs(image, pose_2d, visibility)       
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                   break                           
     outfile.close()
     # When everything done, release the capture
     cap.release()
     cv2.destroyAllWindows()


def display_results(in_image, data_2d, joint_visibility, data_3d):
    """Plot 2D and 3D poses for each of the people in the image."""
    plt.figure()
    draw_limbs(in_image, data_2d, joint_visibility)
    plt.imshow(in_image)
    plt.axis('off')

    # Show 3D poses
    for single_3D in data_3d:
        # or plot_pose(Prob3dPose.centre_all(single_3D))
        plot_pose(single_3D)

    plt.show()

if __name__ == '__main__':
    import sys
    sys.exit(main())
    
