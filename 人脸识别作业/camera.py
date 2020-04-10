#! /usr/bin/env python
import rospy, os, sys
from std_msgs.msg import String
from opencv_apps.msg import FaceArrayStamped
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def callback2(data):
    global x, y, sig, label
    #print(data.faces[0].label)
    lst = data.faces
    
    if len(lst) == 0:
        sig = False
    else:
	label = lst[0].label
        sig = True
        x = lst[0].face.x
        y = lst[0].face.y

def callback(data):
    global x, y, sig, label
    #soundhandle.say("Yes, I can see you")
    #print(data.data)
    if data.data == "CAN YOU SEE ME":
	
        if sig:
            soundhandle.say("Yes, I can see you")
	    print("Yes, I can see you")
        else:
            soundhandle.say("No, I can't see you")
    if data.data == 'DO YOU KNOW WHO IT IS':
        soundhandle.say("Yes, you are %s"% label)
	print("Yes, you are %s"% label)
    if data.data == "I WANT TO TAKE A PICTURE":
	#print(x, y)
        while x > 420 or x < 350:
	    #print(x, y)
	    if sig:
                if x > 420:
                    soundhandle.say("to the left a little")
		    #print("to the left a little")
                    sleep(2)
                elif x < 350:
                    soundhandle.say("to the right a little")
		    #print("to the right a little")
                    sleep(2)
	soundhandle.say("are you ready. Don't move.")
	print("are you ready. Don't move.")
    if data.data == "YES, READY":
        pub = rospy.Publisher('/take_photo', String, queue_size=10)
	#print("Photo already saved.")
	pub.publish("take photo")
    if data.data == "THANK YOU":
	soundhandle.say("it is my pleasure. That is what I do.")


def listener():
    
    rospy.Subscriber('lm_data', String, callback)
    rospy.Subscriber('face_recognition/output', FaceArrayStamped, callback2)
    rospy.spin()

if __name__ == '__main__':
    sig = False
    x = 0
    y = 0
    label = ''
    rospy.init_node('camera', anonymous=True)
    soundhandle = SoundClient()

    rospy.sleep(1)
    
    soundhandle.stopAll()
    listener()
