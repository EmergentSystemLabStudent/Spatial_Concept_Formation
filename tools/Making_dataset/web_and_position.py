#!/usr/bin/env python
# -*- coding:utf-8 -
#*******************************************************
#-------------------------------------------------------
#Author  Satoshi Ishibushi
#date 2015.12.1
#-------------------------------------------------------
# This program is simlutaneously taking picture by web camera 
#and saving the position data of the robot.

#For using this program, you need to install ROS and 
#start the ros master.

#This program make one node which is named "pose_and_img_saver"
#and receive one topic "amcl_pose".

#When it receive the topic, it save data.


#**********************************************************
import cv2
import numpy as np
import sys
import rospy
import os
import argparse
from geometry_msgs.msg import PoseWithCovarianceStamped

parser = argparse.ArgumentParser()
parser.add_argument(
    "Output_directory",
    help="Output directory."
)
parser.add_argument(
    "--init_num",
    default=0,
    type=int,
    help="Initial data number"
)

args = parser.parse_args()
dir =args.Output_directory
# increment for the data number
i=int(args.init_num)

def position_callback(data):
	#sign
	print "getting data"

	global i 

	cap1 = cv2.VideoCapture(1) #The number 1 is device number.


	#saving image
	ret1, img1 = cap1.read()
	cv2.imwrite(dir+'/image/'+str(i)+'.jpg',img1)
		
	print "saving image"+str(i)+".jpg"
	
	#transfoming a quatarnion into a cos,sin data 
	sin= 2*data.pose.pose.orientation.w*data.pose.pose.orientation.z
	cos= data.pose.pose.orientation.w*data.pose.pose.orientation.w - data.pose.pose.orientation.z*data.pose.pose.orientation.z

	#saving prosition data
	f=open(dir+'/position_data/'+repr(i)+'.txt','w')
	f.write(repr(data.pose.pose.position.x)+" "+repr(data.pose.pose.position.y)+"\n")
	f.write(repr(sin)+" "+repr(cos))
	f.close()

	i+=1
	
	
	cap1.release()


 

if __name__ == "__main__":


    os.mkdir(dir)
    os.mkdir(dir+'/position_data')
    os.mkdir(dir+'/image')
    rospy.init_node('pose_and_img_saver', anonymous=True)
    # start sign
    print "OK"
    # reciving the topic  from amcl_node
    #
    rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped,position_callback)
    rospy.spin()

#main()
