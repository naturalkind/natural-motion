import bpy
from mathutils import Vector, Matrix
import numpy as np
import math
from math import radians, ceil

# Importing global modules
import time
import subprocess
import sys
import json
import pickle
import os, random
import numpy as np

argv = sys.argv
argv = argv[-1]
print (argv)


scene = bpy.context.scene


CONNECTIONS = [ [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6], [0, 7], [7, 8],
                [8, 9], [9, 10], [8, 11], [11, 12], [12, 13], [8, 14], [14, 15],
                [15, 16] ]    
                           
LIFTING_BONE_NAMES = ['pelvis_r', 'thigh_r', 'calf_r', 'pelvis_l', 'thigh_l', 'calf_l', 
                      'waist', 'chest', 'neck', 'head', 
                      'shoulder_l', 'arm_l', 'forearm_l', 'shoulder_r', 'arm_r', 'forearm_r']
                      
                      
LIFTING_BONE_PARENTS = {#Right
                        'pelvis_r': 'base',  # основная таз 1
                        'thigh_r': 'pelvis_r', #бедро - таз 2
                        'calf_r': 'thigh_r',  #голень - бедро 3
                        
                        # Left
                        'pelvis_l': 'base',  
                        'thigh_l': 'pelvis_l', 
                        'calf_l': 'thigh_l', 
                        
                         #Туловище
                        'waist': 'base', #основная живот
                        'chest': 'waist', #грудь живот
                        'neck': 'chest',  #
                        'head': 'neck', 
                        'shoulder_l': 'chest', 
                        'arm_l': 'shoulder_l', 
                        'forearm_l': 'arm_l', 
                        'shoulder_r': 'chest', 
                        'arm_r': 'shoulder_r', 
                        'forearm_r': 'arm_r'
                        }   
                          

def create_armature(coordinates, name, scale=1.0):
    """
    Creates an armature skeleton data object from the input coordinates acquired from lift_image(). 
    The skeleton's bones will have been appropriately labelled and parented.
    The skeleton data object will be implemented into the scene as well.
    :param coordinates: List of vertex coordinates from lifter
    :param name: Base name of the bezier_curves 
    :param scale: Scale of the skeleton 
    """
    # Setting the scale to a hundredth already as the distances from lifting are considerably large.
    scale = scale * 0.01  
    arm_dat_name = 'Armature_dat_' + name
    arm_obj_name = 'Armature_obj_' + name
    

    arm_dat = bpy.data.armatures.new(arm_dat_name)
    arm_obj = bpy.data.objects.new(arm_obj_name, arm_dat)
    
    
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    edit_bones = bpy.data.armatures[arm_dat_name].edit_bones
    b = edit_bones.new('base')
    b.head = [coordinates[0][0]*scale, coordinates[0][1]*scale + 100*scale, coordinates[0][2]*scale]
    b.tail = [coordinates[0][0]*scale, coordinates[0][1]*scale,             coordinates[0][2]*scale]
    bone_nr = 0
    FULL_L['base'] = 1.0
    
    for conn in CONNECTIONS:        
        b = edit_bones.new(LIFTING_BONE_NAMES[bone_nr])
        b.head = [scale*item for item in coordinates[conn[0]]]
        b.tail = [scale*item for item in coordinates[conn[1]]]
        b.parent = edit_bones[LIFTING_BONE_PARENTS[str(LIFTING_BONE_NAMES[bone_nr])]]
        b.use_connect = True
        b.length = FULL_L[LIFTING_BONE_NAMES[bone_nr]]
        bone_nr += 1
        
    bpy.ops.object.mode_set(mode='POSE')
    bone_nr = 0
    for conn in CONNECTIONS:    
        
        b = arm_obj.pose.bones[LIFTING_BONE_NAMES[bone_nr]]    
                    
        v1 = Vector(coordinates[conn[0]])
        v2 = Vector(coordinates[conn[1]])    
       
        v = v2 - v1
        v.normalize()
        vGoal = v + b.head           
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.empty_add(type='PLAIN_AXES', location= vGoal)
        target_axis = bpy.context.active_object
        temp_list.append(target_axis.name)
        
        neckCopyRot = arm_obj.pose.bones[LIFTING_BONE_NAMES[bone_nr]].constraints.new('DAMPED_TRACK')  
        neckCopyRot.target = target_axis 
        target_axis.select_set(False) 
        
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode='POSE')   
        bone_nr += 1 
        
    # в режиме редактирования установить позу из режима поз    
    bpy.context.view_layer.objects.active = arm_obj
    bpy.data.objects['Armature_obj_A'].select_set(True)
    bpy.ops.object.mode_set(mode = 'POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode = 'OBJECT')        
        
    return arm_obj
        
        
#Получить координаты скилета
def lift_image(returned_val):
    with open(returned_val) as f:
         f = f.readlines()
         ls = []         
         for i in f:
            ls.append(json.loads(i))
         return ls

# очистить сцену от обьектов
def object_remove():
    bpy.ops.object.delete()     
    for P in bpy.data.objects:
        print ("See", P)
        P.select_set(True) 
        bpy.ops.object.delete()
        
# очистить сцену от арматуры       
def clear_scene(x):
    for P in bpy.data.armatures:
        #print (P.name)
        #bpy.data.armatures.remove(P)
        if P.name == x:
           bpy.data.armatures.remove(P)                                

# увидеть обьекты в сцене        
def object_scene():
    for P in bpy.data.objects:
        print ("See", P)

#------------------------------------------------>

def snap_rotation(source, target):
    Ms = source.id_data.convert_space(
        pose_bone=source,
        matrix=source.matrix,
        from_space='POSE',
        )
    Mt = target.id_data.convert_space(
        pose_bone=target,
        matrix=target.matrix,
        from_space='POSE',
        ) 
         
    _, q, _ = Ms.decompose()
    t, _, s = Mt.decompose()
    M = (
        Matrix.Translation(t) @
        q.to_matrix().to_4x4() @ 
        Matrix.Diagonal(s.to_4d())
        )
    target.matrix = target.id_data.convert_space(
        pose_bone=target,
        matrix=M,
        to_space='POSE',
        )
        
        
def change_arm(coordinates, scale=1.0):
    bpy.ops.object.mode_set(mode='POSE', toggle=False)    

    RIG = bpy.context.active_object.id_data
    bone_nr = 0
    for conn in CONNECTIONS:
        v1 = Vector(coordinates[conn[0]])
        v2 = Vector(coordinates[conn[1]])      
        v = v2 - v1
        v.normalize()

        vGoal = v + ARM.pose.bones[LIFTING_BONE_NAMES[bone_nr]].tail       
        #vGoal = v + ARM.pose.bones[LIFTING_BONE_NAMES[bone_nr]].head
         
        bpy.ops.object.mode_set(mode='OBJECT')
        J = bpy.data.objects[temp_list[bone_nr]]
        J.location = vGoal

        ARM.select_set(True)
        bpy.context.view_layer.objects.active = ARM
        bpy.ops.object.mode_set(mode='POSE')
        
        RIG.data.bones[LIFTING_BONE_NAMES[bone_nr]].select = True
        bpy.ops.pose.visual_transform_apply()
        
        
        
        J.keyframe_insert(data_path="location", frame=frame)
#        ARM.pose.bones[LIFTING_BONE_NAMES[bone_nr]].keyframe_insert(data_path="rotation_euler", frame=frame) 
        ARM.pose.bones[LIFTING_BONE_NAMES[bone_nr]].keyframe_insert(data_path="rotation_quaternion", frame=frame)
        #J.keyframe_insert(data_path="location", frame=frame)
    
        bone_nr += 1                                                          
        scene.frame_set(frame)


#------------------------->
_file = json.loads(open("./static_file/dict_bonse_w.txt", "r").read())
key_w = list(_file.keys())
FULL_L = {}  
for u in LIFTING_BONE_NAMES:
    if "_" in u:
        _key = u.split("_")[0] 
        #print (_key, u, _file[_key])
        FULL_L[u] = _file[_key]
    else:
        FULL_L[u] = _file[u]

#------------------------------------------------>  
    
returned_val = f"./data/{argv}_data_kalman.txt"
coordinates = lift_image(returned_val)

scene.frame_start = 0
scene.frame_end = len(coordinates)

frange = scene.frame_end - scene.frame_start
currframe = scene.frame_start
object_remove()

clear_scene("Armature_dat_A")

temp_list = []
ARM = create_armature(coordinates[0], "A")

#for frame in range(40):
for frame in range(len(coordinates)):
            scene.frame_set(frame)
            COR = coordinates[frame]
            change_arm(COR)


ARM.select_set(False)
bpy.ops.object.mode_set(mode = 'OBJECT')

for _empty in temp_list:
    bpy.data.objects[_empty].select_set(True)
    bpy.ops.object.delete()

scene.frame_set(0)
# Повернуть арматуру на 90 градусов
ARM.select_set(True)
bpy.context.view_layer.objects.active = ARM
bpy.ops.object.mode_set(mode = 'POSE') 

#bpy.context.active_object.rotation_euler[0] = math.radians(90)
#ARM.keyframe_insert(data_path="rotation_euler", frame=0)

#bpy.ops.transform.rotate(value=-math.radians(90), orient_axis='X', orient_type='GLOBAL', 
#                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
#                         orient_matrix_type='GLOBAL', 
#                         constraint_axis=(True, False, False), 
#                         mirror=False, 
#                         use_proportional_edit=False, 
#                         proportional_edit_falloff='SMOOTH', 
#                         proportional_size=1, 
#                         use_proportional_connected=False, 
#                         use_proportional_projected=False, 
#                         release_confirm=True)

ov=bpy.context.copy()
ov['area']=[a for a in bpy.context.screen.areas if a.type=="VIEW_3D"][0]
bpy.ops.transform.rotate(ov, value=math.radians(90), orient_axis='X')

bpy.ops.export_anim.bvh(filepath=f"./file/{argv}.bvh", 
                        check_existing=True, 
                        filter_glob="*.bvh", 
                        global_scale=10, 
                        frame_start=0, frame_end=len(coordinates), rotate_mode='NATIVE', root_transform_only=False)

bpy.ops.wm.quit_blender()


"""
Сделать нейронную сеть обучить на ветрорах движения
Использовать фильтры калмана 
Создать данные, отредактировать фильтром калмана
Обучить использую yolo
Мы находим точку середины кости обрабатываем филтром калмана
Создаем квадрат с центром в точке, полученные данные обучаем в YOLO


вход картинка, данные координат кости, и данные вектора движения

Можно сраху управлять костью

"""

    
    
