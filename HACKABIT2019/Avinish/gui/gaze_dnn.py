#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
import dlib
from math import hypot
import time
from threading import Thread
import playsound
import statistics as st
import pika 
import json
import matplotlib.pyplot as plt


flag=1

def rabbit(msg):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='drowsiness')

    channel.basic_publish(exchange='', routing_key='drowsiness', body=msg)
    connection.close()

def rabbitBLink(msg):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='blink')

    channel.basic_publish(exchange='', routing_key='blink', body=msg)
    connection.close()

def alarm():
    playsound.playsound("alarm.wav")

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

def get_gaze_ratio(eye_points , facial_landmarks,frame):
     # gaze_detector
        eye_region = np.array([(facial_landmarks.part(eye_points[0]).x , facial_landmarks.part(eye_points[0]).y) ,
                                   (facial_landmarks.part(eye_points[1]).x , facial_landmarks.part(eye_points[1]).y ),
                                   (facial_landmarks.part(eye_points[2]).x , facial_landmarks.part(eye_points[2]).y ),
                                   (facial_landmarks.part(eye_points[3]).x , facial_landmarks.part(eye_points[3]).y ),
                                   (facial_landmarks.part(eye_points[4]).x , facial_landmarks.part(eye_points[4]).y ),
                                   (facial_landmarks.part(eye_points[5]).x , facial_landmarks.part(eye_points[5]).y )] , np.int32)
                                   
      
                                           
        #cv2.polylines(frame , [left_eye_region] , True , (0 , 0 , 255) , 1)

        gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        height , width,_ = frame.shape
        mask = np.zeros((height , width) , np.uint8)
        
        cv2.polylines(mask , [eye_region] , True , (0 , 0 , 255) , 1)
        cv2.fillPoly(mask , [eye_region] , 255)
        eye = cv2.bitwise_and(gray , gray , mask = mask)

          
        
        min_x = np.min(eye_region[: , 0])
        max_x = np.max(eye_region[: , 0])
        min_y = np.min(eye_region[: , 1])
        max_y = np.max(eye_region[: , 1])
        
        gray_eye=eye[min_y : max_y , min_x : max_x]
        _, threshold_eye = cv2.threshold(gray_eye , 70 , 255 , cv2.THRESH_BINARY)
        height , width = threshold_eye.shape
        left_side_threshold = threshold_eye[0: height , 0: int(width/2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
        
        right_side_threshold = threshold_eye[0: height , int(width/2) : width]
        right_side_white = cv2.countNonZero(right_side_threshold)
        
        if left_side_white == 0:
            gaze_ratio = 1
        elif right_side_white == 0:
            gaze_ratio = 5
        else:
            gaze_ratio = left_side_white/right_side_white

        return gaze_ratio

class track(Thread):
    def run(self):
        global flag
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        font = cv2.FONT_ITALIC

        total_frame = frame_count = count = blink = frec = 0

        max_drowzy_time = 80

        time_for_blink = 1800
        EYE_R_THRESH = 0.21
        FACE_MAX = 10000 #200*no_of_frames
        counter_face = 0
        avg_face = 0
        s=0
        counter_face1 = 0
        cf_counter = 0
        cb_counter = 0
        blink_frec_5 = []
        NO_FRAMES = 150        
        drowsiness = False
        noFace = False
        start_time = time.time()
        while True:
            if flag == 0:
                break
            frame_count+=1
            _, frame = cap.read()
            gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
            (h,w) = gray.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)), 1.0, (300,300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward() 
            # print(detections.shape)
            cf_counter = cf_counter + 1
            # print("frame {}".format(cf_counter))
            for i in range(0, detections.shape[2]):
                # print(detections)
                # print("hello")
                # FACE DETECTION
                confidence = detections[0,0,i,2]
                if confidence < 0.5:
                    counter_face+=1
                    if counter_face%FACE_MAX==0:
                        if not noFace:
                            rabbit("noFaceStart")
                            noFace = True
                        print("no face")   
                        t=Thread(target=alarm)
                        t.daemon=True
                        t.start()
                        cv2.putText(frame , "NO FACE DETECTED" , (50 , 200) ,font , 4 , (0 , 255 , 0))
                        # t.join()
                    continue
                counter_face = 0
                if noFace:
                   rabbit("noFaceEnd")
                   noFace = False
                box = detections[0,0,i, 3:7]*np.array([w,h,w,h])
                # print(box.shape)
                (startX, startY, endX, endY) = box.astype("int")
                rect = dlib.rectangle(startX, startY, endX, endY)
                text = "{:.2f}".format(confidence*100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                # print("startX : {} startY : {} endX : {} endY : {}".format(startX,startY,endX,endY))
                cv2.rectangle(frame,(startX,startY),(endX,endY),(0,255,0), 2)
                cv2.putText(frame,text, (startX,y),cv2.FONT_HERSHEY_COMPLEX,0.45,(0,255,0),2)

                landmarks = predictor(gray , rect)
                
                left_eye_ratio = get_blinking_ratio([36 , 37 , 38 , 39 , 40 ,41] , landmarks)
                right_eye_ratio = get_blinking_ratio([42 , 43 , 44 , 45 , 46 , 47] , landmarks)
                
                # cf_counter = cf_counter + 1

                if left_eye_ratio < EYE_R_THRESH or right_eye_ratio < EYE_R_THRESH:
                    cb_counter = cb_counter + 1
                    if cf_counter % NO_FRAMES==0:
                        ##  (cb_counter / 600)
                        blink_frec_5.append(cb_counter/600)
                        cf_counter = 0
                        cb_counter = 0
                    cv2.putText(frame , "BLINKING" , (50 , 100) , font , 3 , (255 , 0 , 0) )
                    blink = blink + 1
                    count = count + 1
                    frec = frec + 1
                    # print("eye {}".format(count))
                    if count % max_drowzy_time == 0:
                        if not drowsiness:
                            rabbit("drowStart")
                            drowsiness = True
                        t=Thread(target=alarm)
                        t.daemon=True
                        t.start()
                        cv2.putText(frame , "DROWZINESS DETECTED!!!!!" , (50 , 200) ,font , 4 , (0 , 255 , 0))
                        # t.join()    
                        # print("drow")
                        # count = 0
                    # if frame_count >= time_for_blink:
                    #     blink_frequency = frec / 120
                    #     avg_blink_frequency = (blink * 30) / (total_frame)
                    #     print("avg blink frequency : " , avg_blink_frequency)
                    #     frame_count = 0
                
                else:
                    # print(drowsiness)
                    if drowsiness:
                        rabbit("STOP")
                        drowsiness = False
                    count = 40
                    count-=1

            # frame_count = frame_count +1
            
            # faces = detector(gray)
            # if len(faces)<=0:
            #     counter_face+=1
            #     if counter_face>=FACE_MAX:
            #         cv2.putText(frame,"NO FACE", (10,30), font, 0.7,(0,255,0),1)       
            # for face in faces:
                
                # x , y =face.left() , face.top()
                # x1 , y1 = face.right() , face.bottom()
            ### cv2.rectangle(frame , (x , y) , (x1 , y1) , (0 , 255 , 0) , 2)

                gaze_ratio_left = get_gaze_ratio([36 , 37 , 38 , 39 , 40 ,41] , landmarks,frame)
                gaze_ratio_right = get_gaze_ratio([42 , 43 , 44 , 45 , 46 , 47] , landmarks,frame)
                gaze_ratio = (gaze_ratio_right + gaze_ratio_left)/2

                # if gaze_ratio < 1:
                #     cv2.putText(frame , "right" , (50 , 250) , font , 2 , (0 , 0 , 255) , 3)
                # elif 1< gaze_ratio < 3:
                #     cv2.putText(frame , "center" , (50 , 250) , font , 2 , (0 , 0 , 255) , 3)
                # else:
                #     cv2.putText(frame , "left" , (50 , 250) , font , 2 , (0 , 0 , 255) , 3)
            # cv2.putText(frame , str(gaze_ratio_left) , (50 , 150) , font , 2 , (0 , 0 , 255) , 3)
                #cv2.putText(frame , str(gaze_ratio_right) , (50 , 250) , font , 2 , (0 , 0 , 255) , 3)
                cv2.putText(frame , str(gaze_ratio) , (50 , 150) , font , 2 , (0 , 0 , 255) , 3)
            
            # cv2.imshow("Frame" , frame)
            
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break

        cap.release()
        end_time = time.time()
        elapsed_time = end_time - start_time
        blink_frequency = blink/elapsed_time
        print(elapsed_time)
        print(blink)
        print(blink_frequency)
        print(blink_frec_5)
        # blink_frec_5=[30 , 28  ,29 , 27 , 29 , 26  , 25 , 25,25,24,23,18,16,22,24 , 20 , 21 , 19 , 18 , 15 , 13 , 12 , 9 , 8 , 7 , 6 , 6 , 5 , 6 ,7 ]
        # x = [0,5,10,15,25,30,35,40 , 45 , 50 , 55 , 60 , 65 , 70 , 75, 80 , 85 , 90 , 95 , 100 , 105 , 110 , 115  ,120 , 125 , 130 , 135 , 140 , 145 , 150]
        # y = np.ones([30,])*18
        # y1 = np.ones([30,])*8
        # y2 = np.ones([30,])*24
        # plt.plot(x,blink_frec_5)
        # plt.plot(x,y,label = "average blink frequency")
        # plt.plot(x,y1,label = "fatigue or stress")
        # plt.plot(x,y2,label = "not concentrating")
        # plt.ylabel("blink frequency after each 5 minutes")
        # plt.legend()
        # plt.savefig("plot1.jpg")
        blink_frec_5_j = json.dumps(blink_frec_5)
        # rabbitBLink(blink_frec_5_j)
    def stop(self):
            global flag
            flag = 0
            cv2.destroyAllWindows()
        





