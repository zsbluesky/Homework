#!/usr/bin/env python
import rospy, os, sys
from std_msgs.msg import String
import aiml
from sound_play.msg import SoundRequest

from sound_play.libsoundplay import SoundClient

def callback(data):
    
    rospy.loginfo(data.data)
    global message
    message = data.data

    answer = kernel.respond(message)
    #rospy.loginfo(type(answer))
    if len(answer) > 0:
	pub.publish(answer)
    rate.sleep()
    
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can

    # run simultaneously.


    rospy.Subscriber("lm_data", String, callback)
    #if message == 'hello':
    #rospy.loginfo('123')
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    pub = rospy.Publisher('chatter', String, queue_size=10)
    
    kernel = aiml.Kernel()
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    kernel.learn("std-startup.xml")
    kernel.respond("load aiml b")
    message = ''
    listener()
	
