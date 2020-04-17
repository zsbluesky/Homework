#!/usr/bin/env python

"""

    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location

"""

import rospy

import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler

original = 0
start = 1

class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        
	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

	# Get the initial pose from the user
        rospy.loginfo("*** Click the 2D Pose Estimate button in RViz to set the robot's initial pose...")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)
            
        rospy.loginfo("Ready to go")
	rospy.sleep(1)

	locations = dict()
	while True:
		listener()
		global str, str1
		if str in ["GO TO THE SYSTEM AREA", "GO TO THE ELEVATOR", "GO TO THE EXHIBITION AREA"] and str1 != str:
			str1 = str
			# Location A
			if str == "GO TO THE SYSTEM AREA":
				A_x = -5.05
				A_y = -5.23
				A_theta = 1.5708
			elif str == "GO TO THE ELEVATOR":
				A_x = 6.68
				A_y = 4.94
				A_theta = 1.5708
			elif str == "GO TO THE EXHIBITION AREA":
				A_x = -5.43
				A_y = 6.15
				A_theta = 1.5708

			quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
			locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

			self.goal = MoveBaseGoal()
			rospy.loginfo("Starting navigation test")
			start = 1


			while not rospy.is_shutdown():
			  self.goal.target_pose.header.frame_id = 'map'
			  self.goal.target_pose.header.stamp = rospy.Time.now()

			  # Robot will go to point A
			  if start == 1:
				rospy.loginfo("Going to point A")
				rospy.sleep(2)
				self.goal.target_pose.pose = locations['A']
			  	self.move_base.send_goal(self.goal)
				waiting = self.move_base.wait_for_result(rospy.Duration(300))
				if waiting == 1:
				    rospy.loginfo("Reached point A")
				    rospy.sleep(2)
				    rospy.loginfo("Ready to go back")
				    rospy.sleep(2)
				    global start
				    start = 0

			  # After reached point A, robot will go back to initial position
			  elif start == 0:
				rospy.loginfo("Going back home")
				rospy.sleep(2)
				self.goal.target_pose.pose = self.origin
				self.move_base.send_goal(self.goal)
				waiting = self.move_base.wait_for_result(rospy.Duration(300))
				if waiting == 1:
				    rospy.loginfo("Reached home")
				    rospy.sleep(2)
				    global start
				    start = 2
				    break
				    #global origin
				    #origin = 0

			  #rospy.Rate(5).sleep()

    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()

#import rospy
from std_msgs.msg import String

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global str
    str = data.data

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    #rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("lm_data", String, callback)

if __name__=="__main__":
    rospy.init_node('navi_point')
    str = ""
    str1 = str
	
    try:
	NavToPoint()
	#while True:
	 #   listener()
	  #  if str in ["GO TO THE SYSTEM AREA", "GO TO THE ELEVATOR", "GO TO THE EXHIBITION AREA"] and str1 != str:
	#	print(str)
	#	str1 = str
         #   	NavToPoint(str)
	#	start = 1
	#	origin = 0
        #rospy.spin()
    except:
        pass

