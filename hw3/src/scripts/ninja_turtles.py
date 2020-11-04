#! /usr/bin/python
# https://github.com/clebercoutof/turtle_challenge/blob/master/src/set_goal.py

import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import atan2, sqrt


class NinjaTurtles:
    def __init__(self):
        self.leo_publisher = rospy.Publisher('/leo/cmd_vel', Twist, queue_size=10)
        self.leo_subscriber = rospy.Subscriber('/leo/pose', Pose, self.leo_callback)
        self.trt_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.trt_callback)
        self.leo_pose = Pose()
        self.trt_pose = Pose()

    def leo_callback(self, data):
        self.leo_pose = data
        self.leo_pose.x = round(data.x, 5)
        self.leo_pose.y = round(data.y, 5)
        self.move2goal()

    def trt_callback(self, data):
        self.trt_pose = data
        self.trt_pose.x = round(data.x, 5)
        self.trt_pose.y = round(data.y, 5)
        self.move2goal()

    def distance(self, p1, p2):
        return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def angular(self, p1, p2):
        return atan2(p1.y - p2.y, p1.x - p2.x)


    def move2goal(self, vel=1., thr=0.01):
        vel_msg = Twist()
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0

        dist = self.distance(self.leo_pose, self.trt_pose)
        if dist > thr:
            vel_msg.linear.x = min(dist, vel)
            ang = self.angular(self.trt_pose, self.leo_pose) - self.leo_pose.theta
            if ang == np.pi * 2.:
                ang = np.pi / 8.
            vel_msg.angular.z = 4 * ang

        self.leo_publisher.publish(vel_msg)


if __name__ == '__main__':
    rospy.init_node('ninja_turtles')
    njtrt = NinjaTurtles()
    rospy.spin()

