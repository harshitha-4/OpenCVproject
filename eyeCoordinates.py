#!/home/naina4/.virtualenvs/cv/bin/python
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound

import argparse
import imutils
import time
import dlib
import cv2
import pygame

import time
from Tkinter import *


def sound_alarm(path):
    # play an alarm sound

    pygame.init()

    pygame.mixer.music.load("alarm.wav")

    pygame.mixer.music.play()

    time.sleep(10)


# playsound.playsound(path)

def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear
def mouth_distance(mouth):
    P=dist.euclidean(mouth[1],mouth[3])


    return P

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
                help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 48

COUNTER = 0
ALARM_ON = False


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# start the video stream thread
print("[INFO] startingo4 video stream thread...")
vs = VideoStream(1).start()
time.sleep(1.0)


# loop over frames from the video stream
while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=850)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:

        shape = predictor(gray, rect)
        x1=(float(shape.part(63).x))
        y1=(float(shape.part(63).y))
        x2=float(shape.part(67).x)
        y2=float(shape.part(67).y)
        D = dist.euclidean((x1, y1), (x2, y2))
        shape = face_utils.shape_to_np(shape)


        mouth=shape[48:68]
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        mouthHull=cv2.convexHull(mouth)
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (135,206,250), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (135,206,250), 1)
        cv2.drawContours(frame,[mouthHull],-1,(139,0,0),1)

        if ear < EYE_AR_THRESH:
            COUNTER += 1

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True

                    if args["alarm"] != "":
                        t = Thread(target=sound_alarm,
                                   args=(args["alarm"],))
                        t.deamon = True
                        t.start()

                # draw an alarm on the frame
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        elif D>43 and ear>EYE_AR_THRESH:
            if not ALARM_ON:
                ALARM_ON = True

                if args["alarm"] != "":
                    t = Thread(target=sound_alarm,
                               args=(args["alarm"],))
                    t.deamon = True
                    t.start()

                    # draw an alarm on the frame
            cv2.putText(frame, "YAWNING ALERT!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            COUNTER=0
            ALARM_ON=False

        #cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
        #           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()