#!/usr/bin/env python

import rospy
import math
from location_monitor.msg import LandmarkDistance
from nav_msgs.msg import Odometry



def distance(x1, y1, x2, y2):
	xd = x1 - x2
	yd = y1 - y2
	return math.sqrt(xd*xd + yd*yd)


class LandmarkMonitor(object):
	def __init__(self, pub, landmarks):
		self._pub = pub
		self._landmarks = landmarks

	def callback(self, msg):
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		# rospy.loginfo('x: {}, y: {}'.format(x,y))
		closests_name = None
		closests_distance = None 
		for l_name, l_x, l_y in self._landmarks:
			dist = distance(x,y, l_x, l_y)
			if closests_distance is None or dist < closests_distance:
				closests_name = l_name
				closests_distance = dist

				# rospy.loginfo('l_name: {} l_x: {}, l_y: {}'.format(l_name, l_x, l_y ))
				# rospy.loginfo('l_name: {} l_x: {}, l_y: {}'.format(l_name, l_x, l_y ))
		# rospy.loginfo('dist ({}) < c losests_distance {} || closest: {}  || x: {}, y: {}'.format(dist, closests_distance, closests_name, x,y))
		
		ld = LandmarkDistance()
		ld.name = closests_name
		ld.distance = closests_distance
		self._pub.publish(ld)

		# rospy.loginfo('closest {}'.format(closests_name)) 


def main():
	rospy.init_node('location_monitor')

	landmarks = []
	landmarks.append(("Cube", 0.31, -0.99))
	landmarks.append(("Dumpster", 0.11, -2.42))
	landmarks.append(("Cylinder", -1.14, -2.88))
	landmarks.append(("Barrier", -2.59, -0.83))
	landmarks.append(("Bookshelf", 0.09, 0.53))

	# pub = rospy.Publisher('closests_landmark', LandmarkDistance) #error
	pub = rospy.Publisher('closests_landmark', LandmarkDistance, queue_size =10)
	monitor = LandmarkMonitor(pub, landmarks)
	rospy.Subscriber("/odom", Odometry, monitor.callback)
	rospy.spin()


if __name__ == '__main__':
	main()