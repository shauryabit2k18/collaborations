#!/usr/bin/env python
# coding: utf-8



import cv2
import numpy as np
import dlib
from math import hypot

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_ITALIC

total_frame = frame_count = count = blink =frec = 0

max_drowzy_time = 150

time_for_blink = 1800


def get_blinking_ratio(eye_points , facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x , facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x , facial_landmarks.part(eye_points[3]).y)
        
        #hor_line = cv2.line(frame , left_point , right_point , (0 , 255 , 0) , 1)
        
        top_point = (int((facial_landmarks.part(eye_points[2]).x + facial_landmarks.part(eye_points[1]).x)/2) , int((facial_landmarks.part(eye_points[2]).y + facial_landmarks.part(eye_points[1]).y)/2))
        bottom_point = (int((facial_landmarks.part(eye_points[5]).x + facial_landmarks.part(eye_points[4]).x)/2) , int((facial_landmarks.part(eye_points[5]).y + facial_landmarks.part(eye_points[4]).y)/2))
        
        #ver_line = cv2.line(frame , top_point , bottom_point , (0 , 255 , 0) , 1)
        
        ver_line_length = hypot((top_point[0] - bottom_point[0]) , (top_point[1] - bottom_point[1]))
        hor_line_length = hypot((left_point[0] - right_point[0]) , (left_point[1] - right_point[1]))
        

        ratio =  ver_line_length / hor_line_length
        
        return ratio

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    
    frame_count = frame_count +1
    
    faces = detector(gray)
    for face in faces:
        
        # x , y =face.left() , face.top()
        # x1 , y1 = face.right() , face.bottom()
       ### cv2.rectangle(frame , (x , y) , (x1 , y1) , (0 , 255 , 0) , 2)
        
        landmarks = predictor(gray , face)
        
        left_eye_ratio = get_blinking_ratio([36 , 37 , 38 , 39 , 40 ,41] , landmarks)
        right_eye_ratio = get_blinking_ratio([42 , 43 , 44 , 45 , 46 , 47] , landmarks)
        
        if left_eye_ratio < 0.21 or right_eye_ratio < 0.21:
            cv2.putText(frame , "BLINKING" , (50 , 100) , font , 3 , (255 , 0 , 0) )
            blink = blink + 1
            count = count + 1
            frec = frec + 1
            if count >= max_drowzy_time:
                cv2.putText(frame , "DROWZINESS DETECTED!!!!!" , (50 , 200) ,font , 4 , (0 , 255 , 0))
                count = 0
            if frame_count >= time_for_blink:
                blink_frequency = frec / 120
                avg_blink_frequency = (blink * 30) / (total_frame)
                print("avg blink frequency : " , avg_blink_frequency)
                frame_count = 0
        
        else:
            count = 0
            
        # gaze_detector
        left_eye_region = np.array([(landmarks.part(36).x , landmarks.part(36).y) ,
                                   (landmarks.part(37).x , landmarks.part(37).y ),
                                   (landmarks.part(38).x , landmarks.part(38).y ),
                                   (landmarks.part(39).x , landmarks.part(39).y ),
                                   (landmarks.part(40).x , landmarks.part(40).y ),
                                   (landmarks.part(41).x , landmarks.part(41).y )] , np.int32)
        
        #cv2.polylines(frame , [left_eye_region] , True , (0 , 0 , 255) , 1)
        
        height , width,_ = frame.shape
        mask = np.zeros((height , width) , np.uint8)
        
        cv2.polylines(mask , [left_eye_region] , True , (0 , 0 , 255) , 1)
        cv2.fillPoly(mask , [left_eye_region] , 255)
        left_eye = cv2.bitwise_and(gray , gray , mask = mask)
        
        
        min_x = np.min(left_eye_region[: , 0])
        max_x = np.max(left_eye_region[: , 0])
        min_y = np.min(left_eye_region[: , 1])
        max_y = np.max(left_eye_region[: , 1])
        
        gray_eye=left_eye[min_y : max_y , min_x : max_x]
        _, threshold_eye = cv2.threshold(gray_eye , 70 , 255 , cv2.THRESH_BINARY)
        height , width = threshold_eye.shape
        left_side_threshold = threshold_eye[0: height , 0: int(width/2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
        
        right_side_threshold = threshold_eye[0: height , int(width/2) : width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        
        if right_side_white !=0:
            gaze_ratio = left_side_white/right_side_white
            cv2.putText(frame , str(gaze_ratio) , (50 , 150) , font , 2 , (0 , 0 , 255) , 3)
        
        eye = cv2.resize(gray_eye , None , fx = 5 , fy = 5)
        threshold_eye = cv2.resize(threshold_eye , None , fx = 5 , fy = 5)
        
        cv2.imshow("Eye" , eye)
        cv2.imshow("Threshold" , threshold_eye)
        cv2.imshow("left_eye" , left_eye)
    
    cv2.imshow("Frame" , frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()

