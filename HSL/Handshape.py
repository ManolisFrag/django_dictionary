import numpy as np
import json
import os
from math import *
from math import pi as pii
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')
from scipy.spatial import distance

def scale_x(x_array, min_array_x, max_array_x):
    OldMax = max_array_x
    OldMin = min_array_x
    NewMax = 1
    NewMin = -1
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)
    Newx = []
    for OldValuex in x_array:
        NewValue = (((OldValuex - OldMin) * NewRange) / OldRange) + NewMin
        Newx.append(NewValue)
    return Newx

def scale_y(y_array, min_array_y, max_array_y):    
    Newy = []    
    OldMax = max_array_y
    OldMin = min_array_y
    NewMax = 1
    NewMin = -1
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)
    for OldValuey in y_array:
        NewValuey = (((OldValuey - OldMin) * NewRange) / OldRange) + NewMin
        Newy.append(NewValuey)
    return Newy

def getAngle(A,B):
    
    deltaY = abs(B[1] - A[1]);
    deltaX = abs(B[0] - A[0]);

    angleInDegrees = atan2(deltaY, deltaX) * 180 / pi
    print("AngleINDegrees raw is: ", angleInDegrees)
    if(B[1] > A[1]):

        if(B[0] < A[0]):
            print("case 1")
            angleInDegrees += 180;
        else: 
            print("case 2")
            angleInDegrees += 270;

    elif (B[0] < A[0]):
        print("case 3")
        angleInDegrees += 90;

    return(angleInDegrees)


def angle_c(x1,y1,x2,y2):
    if x1==x2:
        if (y2 > y1):
            result = 0.5 * pii
        else:
            result = 1.5 * pii
    result = atan((y2-y1)/(x2-x1))
    if (x2 < x1):
        result = result + pii
    if (result < 0):
        result = result + 2*pii
    result = result * 180/pii
    return(result)
        
            
    
def get_arm_angle_from_json(json_file_path):
    with open(json_file_path) as f:
        loaded_json = json.load(f)
        raw_coords = loaded_json["people"][0]["pose_keypoints_2d"]
        #remove confidence values
        raw_coords = np.delete(raw_coords, np.arange(2, len(raw_coords), 3))
        raw_coords = np.reshape(raw_coords, (25,2))

        raw_coords = np.array(raw_coords)
        arm_coords = np.array([raw_coords[3],raw_coords[4]])
        #print(arm_coords[0][0],arm_coords[0][1], arm_coords[1][0], arm_coords[1][0])
       
        return(angle_c(arm_coords[0][0],arm_coords[0][1], arm_coords[1][0], arm_coords[1][1]))
    
def get_left_fingers_from_json(json_file_path):
    """
    function to open a json file and return the x,y positions of the fingers of the left hand.
    Provide the path to the json file
    """
    with open(json_file_path) as f:
        loaded_json = json.load(f)
        person = loaded_json["people"]
        if person:
            raw_coords = loaded_json["people"][0]["hand_left_keypoints_2d"]
            #remove confidence values
    #         raw_coords = np.delete(raw_coords, np.arange(2, len(raw_coords), 3))
            raw_coords = np.reshape(raw_coords, (21,3))

            raw_coords = np.array(raw_coords)

            scaled_x = scale_x(raw_coords[:,[0]], min(raw_coords[:,[0]]), max(raw_coords[:,[0]]))
            scaled_y = scale_y(raw_coords[:,[1]], min(raw_coords[:,[1]]), max(raw_coords[:,[1]]))
            confidence_left = raw_coords[:,[2]]
            return(scaled_x,scaled_y,confidence_left) 
        
## rotate hand
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy

    

class handshape(object):
    
    def __init__(self, json_file_path):
        self._json_file_path = json_file_path
    
    @property
    def get_right_fingers_from_json(self):
        """
        function to open a json file and return the x,y positions of the fingers of the left hand.
        Provide the path to the json file
        """
        with open(self._json_file_path) as f:
            loaded_json = json.load(f)
            person = loaded_json["people"]
            if person:
                raw_coords = loaded_json["people"][0]["hand_right_keypoints_2d"]
                
                #scale based on the whole body coordinates
                whole_body_coords = loaded_json["people"][0]["pose_keypoints_2d"]
                
                whole_body_coords = np.delete(whole_body_coords, np.arange(2, len(whole_body_coords), 3))
                whole_body_coords = np.reshape(whole_body_coords, (25,2))
                
                whole_body_coords = np.array([whole_body_coords[0], whole_body_coords[1], whole_body_coords[2], whole_body_coords[3], whole_body_coords[4], whole_body_coords[5], whole_body_coords[6], whole_body_coords[7], whole_body_coords[15], whole_body_coords[16], whole_body_coords[17], whole_body_coords[18]])
                
                hands = whole_body_coords
    
                hands2 = hands - hands[0][0]
                #get the x values
                handsx = hands2[:,0]
                #get y values
                handsy = hands2[:,1]
                scaledY = handsy - hands2[0][1]
                scaledHands = np.array((handsx,scaledY))
                scaledHands = scaledHands.T

                dist = distance.euclidean(scaledHands[2], scaledHands[5])
                final_scaled = scaledHands/dist
                
                
                ######

                raw_coords = np.reshape(raw_coords, (21,3))

                raw_coords = np.array(raw_coords)

#                 scaled_x = scale_x(raw_coords[:,[0]], min(raw_coords[:,[0]]), max(raw_coords[:,[0]]))
#                 scaled_y = scale_y(raw_coords[:,[1]], min(raw_coords[:,[1]]), max(raw_coords[:,[1]]))
                confidence_right = raw_coords[:,[2]]
    
    
                ###added code
                
#                 raw_coords = np.delete(raw_coords, np.arange(2, len(raw_coords), 3))
                raw_coords = np.delete(raw_coords, np.arange(2, raw_coords.size, 3))
                raw_coords = np.reshape(raw_coords, (21,2))
               
                
                shift_x = raw_coords - hands[0][0]
                
                
                scaled_x = shift_x[:,0]
                
                shift_y = shift_x[:,1]
                scaled_y = shift_y - shift_x[0][1]
                
                #ara exw scaled_x kai scaled_y
                
                
        
                #####

                #get angle of arm from json
                rotation = get_arm_angle_from_json(self._json_file_path)

                #debug: plot scalled coordinates
    #             plt.scatter(scaled_x, scaled_y, s=(20 * confidence_right)**2, alpha = 0.7)
    #             plt.show()

                pi=22/7
                rotated_hand_coords = []
                for i in range (len(scaled_x)):
#                     rotated_hand_coords.append(rotate((scaled_x[i][0],scaled_y[i][0]), (0,0), radians(rotation*(pi/180))))
                    rotated_hand_coords.append(rotate((scaled_x[i],scaled_y[i]), (0,0), radians(rotation*(pi/180))))
                rotated_hand_coords = np.array(rotated_hand_coords)
#                 print("index",rotated_hand_coords[7])

                return(rotated_hand_coords, confidence_right)
#                 return([scaled_x,scaled_y],confidence_right) 
            else:
                pass
