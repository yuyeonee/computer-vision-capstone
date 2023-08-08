from database import Client
import dlib
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from gaze_tracking import GazeTracking
from datetime import datetime
import time

cl=Client()

data_understand = {
    "s_id":"",
    "name":"",
    "understand":0
}

data_attention = {
    "s_id":"",
    "name":"",
    "attention":0
}

name=input("이름 입력 : ")
id=input("학번 입력 : ")

data_understand["name"]=name
data_understand["s_id"]=id
data_attention["name"]=name
data_attention["s_id"]=id

#print(data_understand)
#print(data_attention)


gaze = GazeTracking()

# face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_81_face_landmarks.dat")

model_top = load_model('models/ResNet50_3_newdata5_400.h5')
EMOTION_DICT = {1: 'happy', 0: 'confused', 2: 'neutral'}


# 눈으로 영상 보면서 확인할 때/
def face_classification():
    emotion_label_list = []
    attention_list=[]
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:
        ret, img = cap.read()
        face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            face_clip = img[y:y + h, x:x + w]
            face_resize = cv2.resize(face_clip, (224, 224))
            face_image = face_resize.reshape(1, face_resize.shape[0], face_resize.shape[1], face_resize.shape[2])

            top_pred = model_top.predict(face_image)
            emotion_label = top_pred[0].argmax()
            pre_emotion = EMOTION_DICT[emotion_label]

            cv2.putText(img, pre_emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            emotion_label_list.append(emotion_label)
            #print(top_pred,emotion_label,pre_emotion)

        now_time=time.time()
        elapsed_time = now_time - start_time
        if elapsed_time >=30:
            start_time=now_time
            #print(emotion_label_list.count(0))
            #print(len(emotion_label_list))
            confused_count=emotion_label_list.count(0)
            if confused_count==0:
                percent_u=0
            else:
                percent_u = emotion_label_list.count(0)/len(emotion_label_list)

            if percent_u>=0.5:
                data_understand["understand"]=1
            else:
                data_understand["understand"]=0
            cl.write_understand(data_understand)
            emotion_label_list=[]


        # We send this frame to GazeTracking to analyze it

        gaze.refresh(img)

        img = gaze.annotated_frame()
        text1 = ""

        if gaze.is_blinking():
            attention_list.append(1)
            text1='close'
        elif gaze.is_right():
            attention_list.append(0)
            text1 = "open"
        elif gaze.is_left():
            attention_list.append(0)
            text1 = "open"
        elif gaze.is_center():
            attention_list.append(0)
            text1 = "open"
        else :
            attention_list.append(0)
            text1 = "open222222222222"

        print("Blinking: ",text1)
        cv2.imshow('img', img)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            return attention_list

    cap.release()
    cv2.destroyAllWindows()

attention_list=face_classification()

percent_a = attention_list.count(0)/len(attention_list)
data_attention["attention"]=percent_a
cl.write_attention(data_attention)