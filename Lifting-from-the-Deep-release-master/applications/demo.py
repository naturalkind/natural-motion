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
    image = cv2.imread(IMAGE_FILE_PATH)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb

    # create pose estimator
    image_size = image.shape

    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

    # load model
    pose_estimator.initialise()

    try:
        # estimation
        outfile = open('data_c.txt', 'w')
        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
        for ii in pose_3d:
                coordinates = []
                #print len(ii[2])#len(pose_3d[ii][0], len(pose_3d[ii][1]), len(pose_3d[ii][2])) 
                for i in range(len(ii[0])):
                    #print ii[2][i]#len()
                    coordinates.append([ii[0][i], ii[1][i], ii[2][i]])
                    #coordinates.append([pose_3d[ii][i][0], pose_3d[ii][i][1], pose_3d[ii][i][2]])
                    #for point in pose_3d[ii]:
                    #       coordinates.append([point[i], point[i], point[i]])
                           #print point[0][i], point[1][i], point[2][i]
                #print len(coordinates), len(pose_3d[ii][0]), len(pose_3d[0])           
                outfile.write(str(coordinates)+"\n") 
                #outfile.write("\n")
        outfile.close()                
#        # estimation
#        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
#        coordinates = []
#        for i in range(len(pose_3d[0][0])):
#            for point in pose_3d:
#                   coordinates.append([point[0][i], point[1][i], point[2][i]])
#                   #print point[0][i], point[1][i], point[2][i]
#        with open('data_c.txt', 'w') as outfile:
#               json.dump(coordinates, outfile)  
#        # Show 2D and 3D poses
#        display_results(image, pose_2d, visibility, pose_3d)
        
        #Save Resul
    except ValueError:
        print('No visible people in the image. Change CENTER_TR in packages/lifting/utils/config.py ...')

    # close model
    pose_estimator.close()


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
    
#def main():
#    image = cv2.imread(IMAGE_FILE_PATH)
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb

#    # create pose estimator
#    image_size = image.shape

#    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

#    # load model
#    pose_estimator.initialise()

#    try:
#        # estimation
#        pose_2d, visibility, pose_3d = pose_estimator.estimate(image)
#        coordinates_peron = ""
#        F = open('data_c.txt', 'w')
#       
#        for i in range(len(pose_3d[0][0])):
#             coordinates = "["
#             for point in pose_3d:
#                 t_str = "[{}, {}, {}],".format(str(point[0][i]), str(point[1][i]), str(point[2][i]))
#                 coordinates = coordinates + t_str
#             coordinates = coordinates + "]\n" 
#             F.write(coordinates)  
##            coordinates = []
##            for point in pose_3d:
##                   coordinates.append([point[0][i], point[1][i], point[2][i]])
##                   #print point[0][i], point[1][i], point[2][i]
##            #coordinates_peron.append(coordinates) 
##            F.write(str(coordinates)+"\n") 
#            #F.write("\n")
#            #coordinates_peron += str(coordinates) + "\n"      
#        #with open('data_c.txt', 'w') as outfile:
#               #outfile.write(str(coordinates)+"\n") 
#               #outfile.write()
#               #json.dump(coordinates_peron, outfile)  
#        # Show 2D and 3D poses
#        #display_results(image, pose_2d, visibility, pose_3d)
#        
#        #Save Resul
#    except ValueError:
#        print('No visible people in the image. Change CENTER_TR in packages/lifting/utils/config.py ...')

#    # close model
#    pose_estimator.close()


#def display_results(in_image, data_2d, joint_visibility, data_3d):
#    """Plot 2D and 3D poses for each of the people in the image."""
#    plt.figure()
#    draw_limbs(in_image, data_2d, joint_visibility)
#    plt.imshow(in_image)
#    plt.axis('off')

#    # Show 3D poses
#    for single_3D in data_3d:
#        # or plot_pose(Prob3dPose.centre_all(single_3D))
#        plot_pose(single_3D)

#    plt.show()

#if __name__ == '__main__':
#    import sys
#    sys.exit(main())    
