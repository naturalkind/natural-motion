import json

class KalmanFilter:
    def __init__(self):  
      	# значение инициализации
        self.x_P = 0.9
        self.x_Q = 0.08
        
        self.y_P = 0.9
        self.y_Q = 0.08
        
        self.z_P = 0.9
        self.z_Q = 0.08
        
        self.x_priori_estimated_covariance = 1 
        self.y_priori_estimated_covariance = 1
        self.z_priori_estimated_covariance = 1
        # X 
        self.x_estimated_value_dict = {'base': 0, 'pelvis_r': 0, 'thigh_r': 0, 'calf_r': 0, 'pelvis_l': 0, 
                                       'thigh_l': 0, 'calf_l': 0, 'waist': 0, 'chest': 0, 
                                       'neck': 0, 'head': 0, 'shoulder_l': 0, 'arm_l': 0, 
                                       'forearm_l': 0, 'shoulder_r': 0, 'arm_r': 0, 'forearm_r': 0}

        self.x_post_estimated_covariance_dict = {'base': 1, 'pelvis_r': 1, 'thigh_r': 1, 'calf_r': 1, 'pelvis_l': 1, 
                                                 'thigh_l': 1, 'calf_l': 1, 'waist': 1, 'chest': 1, 
                                                 'neck': 1, 'head': 1, 'shoulder_l': 1, 'arm_l': 1, 
                                                 'forearm_l': 1, 'shoulder_r': 1, 'arm_r': 1, 'forearm_r': 1}
        # Y 
        self.y_estimated_value_dict = {'base': 0, 'pelvis_r': 0, 'thigh_r': 0, 'calf_r': 0, 'pelvis_l': 0, 
                                       'thigh_l': 0, 'calf_l': 0, 'waist': 0, 'chest': 0, 
                                       'neck': 0, 'head': 0, 'shoulder_l': 0, 'arm_l': 0, 
                                       'forearm_l': 0, 'shoulder_r': 0, 'arm_r': 0, 'forearm_r': 0}

        self.y_post_estimated_covariance_dict = {'base': 1, 'pelvis_r': 1, 'thigh_r': 1, 'calf_r': 1, 'pelvis_l': 1, 
                                                 'thigh_l': 1, 'calf_l': 1, 'waist': 1, 'chest': 1, 
                                                 'neck': 1, 'head': 1, 'shoulder_l': 1, 'arm_l': 1, 
                                                 'forearm_l': 1, 'shoulder_r': 1, 'arm_r': 1, 'forearm_r': 1}
                                                 
        # Z                                         
        self.z_estimated_value_dict = {'base': 0, 'pelvis_r': 0, 'thigh_r': 0, 'calf_r': 0, 'pelvis_l': 0, 
                                       'thigh_l': 0, 'calf_l': 0, 'waist': 0, 'chest': 0, 
                                       'neck': 0, 'head': 0, 'shoulder_l': 0, 'arm_l': 0, 
                                       'forearm_l': 0, 'shoulder_r': 0, 'arm_r': 0, 'forearm_r': 0}

        self.z_post_estimated_covariance_dict = {'base': 1, 'pelvis_r': 1, 'thigh_r': 1, 'calf_r': 1, 'pelvis_l': 1, 
                                                 'thigh_l': 1, 'calf_l': 1, 'waist': 1, 'chest': 1, 
                                                 'neck': 1, 'head': 1, 'shoulder_l': 1, 'arm_l': 1, 
                                                 'forearm_l': 1, 'shoulder_r': 1, 'arm_r': 1, 'forearm_r': 1}

    # перезагрузка значений
    def x_reset(self, P, Q): 
        self.x_P = P
        self.x_Q = Q

    def y_reset(self, P, Q):
        self.y_P = P
        self.y_Q = Q

    def z_reset(self, P, Q):
        self.z_P = P
        self.z_Q = Q

    # входные текущие значения поступающие в фильтр   
    def cal_X(self, current_value, label):  
        self.current_value = current_value
        self.x_priori_estimated_covariance = self.x_post_estimated_covariance_dict[label]
        x_kalman_gain = self.x_priori_estimated_covariance / (self.x_priori_estimated_covariance + self.x_P)  
        output = self.x_estimated_value_dict[label] + x_kalman_gain * (
                    current_value - self.x_estimated_value_dict[label])  
        self.x_estimated_value_dict[label] = output
        self.x_post_estimated_covariance_dict[label] = (1 - x_kalman_gain) * self.x_priori_estimated_covariance + self.x_Q
        self.x_priori_estimated_covariance = self.x_post_estimated_covariance_dict[label]
        return output  

    def cal_Y(self, current_value, label):  
        self.current_value = current_value
        self.y_priori_estimated_covariance = self.y_post_estimated_covariance_dict[label]
        y_kalman_gain = self.y_priori_estimated_covariance / (self.y_priori_estimated_covariance + self.y_P)  
        output = self.y_estimated_value_dict[label] + y_kalman_gain * (
                    current_value - self.y_estimated_value_dict[label])  
        self.y_estimated_value_dict[label] = output
        self.y_post_estimated_covariance_dict[label] = (1 - y_kalman_gain) * self.y_priori_estimated_covariance + self.y_Q
        self.y_priori_estimated_covariance = self.y_post_estimated_covariance_dict[label]
        return output

    def cal_Z(self, current_value, label): 
        self.current_value = current_value
        self.z_priori_estimated_covariance = self.z_post_estimated_covariance_dict[label]
        z_kalman_gain = self.z_priori_estimated_covariance / (self.z_priori_estimated_covariance + self.z_P)  
        output = self.z_estimated_value_dict[label] + z_kalman_gain * (
                    current_value - self.z_estimated_value_dict[label])  
        self.z_estimated_value_dict[label] = output
        self.z_post_estimated_covariance_dict[label] = (1 - z_kalman_gain) * self.z_priori_estimated_covariance + self.z_Q
        self.z_priori_estimated_covariance = self.z_post_estimated_covariance_dict[label]
        return output


class KalmanProcess():
    def __init__(self):
        self.kalman_filter_X = KalmanFilter()
        self.kalman_filter_Y = KalmanFilter()
        self.kalman_filter_Z = KalmanFilter()

    def reset_kalman_filter_X(self, P, Q):
        self.kalman_filter_X.x_reset(P, Q)

    def reset_kalman_filter_Y(self, P, Q):
        self.kalman_filter_Y.y_reset(P, Q)

    def reset_kalman_filter_Z(self, P, Q):
        self.kalman_filter_Z.z_reset(P, Q)


    def do_kalman_filter(self, X, Y, Z, label):
        X_cal = self.kalman_filter_X.cal_X(X, label)
        Y_cal = self.kalman_filter_Y.cal_Y(Y, label)
        Z_cal = self.kalman_filter_Z.cal_Z(Z, label)
        return X_cal, Y_cal, Z_cal
      
kalman_process = KalmanProcess()

_dict = {'base': 0, 'pelvis_r': 0, 'thigh_r': 0, 'calf_r': 0, 'pelvis_l': 0, 
         'thigh_l': 0, 'calf_l': 0, 'waist': 0, 'chest': 0, 
         'neck': 0, 'head': 0, 'shoulder_l': 0, 'arm_l': 0, 
         'forearm_l': 0, 'shoulder_r': 0, 'arm_r': 0, 'forearm_r': 0}

list_dict = list(_dict.keys())   
#Получить координаты скилета
def lift_image(returned_val):
    with open(returned_val) as f:
         f = f.readlines()
         ls = []         
         for i in f:
            ls.append(json.loads(i))
         return ls
         
returned_val = "data_c.txt"
coordinates = lift_image(returned_val)
_file = open("data_c_kalman_1.txt","w")
for i in coordinates:
    coordinates = []
    for iz, z in enumerate(i):
        out_kalman_x, out_kalman_y, out_kalman_z = kalman_process.do_kalman_filter(z[0], z[1], z[2], list_dict[iz])
        coordinates.append([out_kalman_x, out_kalman_y, out_kalman_z])
    _file.write(str(coordinates)+"\n")  
_file.close()      
