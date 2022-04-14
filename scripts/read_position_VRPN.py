#!/usr/bin/env python3

import rospy # the ROS api for python. We need it to create a node, 
             # a subscriber and access other ROS-specific program control
from geometry_msgs.msg import PoseStamped


rospy.init_node("extra_message_node")
print("Now")
msg = rospy.wait_for_message("/vrpn_client_node/Wand/pose", PoseStamped)

print("fin")
print ("Full message: \n")
print (msg) # that's the whole Odometry message. It should be something like
            # what was printed out by `rosmsg show nav_msgs/Odometry`

# print out each of the parent variables
print ("\n Parent variables: \n")
print (msg.pose)
# print msg.child_frame_id
# print msg.pose
# print msg.twist

# print some children
print ("\nSome children: \n")
print (msg.pose.position)
# print msg.pose.pose
# print msg.twist.twist

# print out some grandchildren
print ("\nSome grandchildren: \n")
print (msg.pose.position.x)
# print msg.twist.twist.linear

# # print out some great grandchildren :)
# print "\nSome great grandchildren: \n"
# print msg.pose.pose.orientation.w
# print msg.twist.twist.angular.z

# # print other (great grand) children below this line
# print "\nOther ones you have specified: \n"
