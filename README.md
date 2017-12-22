**Drowsiness_Detection**</br></br>
Drowsiness_Detection is a fatigue detection system that alerts users when they are falling asleep.</br>
It uses your computer's webcam to detect Eyes and mouth features using facial_landmarks. If your eyes
stay closed for long periods of time or yawning is detected, then the program lets you know using an
alarm sound.</br></br>
**SYSTEM REQUIREMENTS**:</br></br>
Eye-Spy should work on any OSX, Linux or Windows system with a webcam and a minimum of
4GB RAM .</br></br>
**DEPENDENCIES**:</br></br>
The code was run with OpenCV 3.0.0 and Python 2.7.12 .</br>
The following python modules should be downoaded and installed:</br>
numpy</br>
SciPy</br>
pip</br>
dlib</br>
cv2</br>
playsound</br>
imutils</br>
pygame</br></br>
**CODE OVERVIEW**:</br></br>
**1**.
Using 68 facial landmarks which is available in dlib library,eye coordinates and mouth
coordinates are calculated.</br>
**2**. looping over frames from the video stream :
In an infinate loop,(x,y) coordinates are converted into numpy array for mathematical
calculation.</br>
Euclidean distance is calculated between (x,y) coordinates of mouth .</br>
**3**.**Eye Aspect Ratio**: EAR is calculated and if it is more than the Threshold
value(EYE_AR_THRESH) meaning that eyes are closed, counter value is incremented to
calculate the amount of time it is closed.</br>
If the value of counter is more than the Threshold time(EYE_AR_CONSEC_FRAMES) meaning
that the eyes are closed for more than threshold time,then an alarm is used to alert the user.
Similarly for the yawning detection,if the euclidean distance between mouth coordinates is
more,then an alarm is used to alert the user.</br>
**4**.**GUI**: Graphical User Interface is created using Tkinter.
