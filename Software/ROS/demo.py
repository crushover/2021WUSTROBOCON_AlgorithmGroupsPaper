#! /usr/bin/env python
import math
import rospy
from geometry_msgs.msg import Twist


if __name__ == "__main__":
    # 2.初始化 ROS 节点
    rospy.init_node("control_circle_p")
    # 3.创建发布者对象
    pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=1000)
    # 4.循环发布运动控制消息
    rate = rospy.Rate(10)
    msg = Twist()

    i = 0
    a = 0
    b = 0
    t = 0
    k = 0
    # a = 1
    # b = 1.5
    

    while not rospy.is_shutdown():
        # theta = ((i/180)*math.pi)
        # a = 0.3 * math.sqrt(math.fabs(2*math.cos(theta))*math.fabs(math.cos(theta)))
        # b = math.sqrt(math.fabs(2*math.cos(theta))*math.fabs(math.sin(theta)))
        t = float((i/180.0)*math.pi)

        if t >0 and t <= (math.pi)/4 :
            a = math.sqrt(2*math.cos(2*t)) * (math.cos(t))
            b = math.sqrt(2*math.cos(2*t)) * (math.sin(t))

            k = 3*(math.sqrt(a**2+b**2))
            c = float(a*2)
            d = float(b*2)
            msg.linear.x = 1.2       
            msg.angular.z = k*1.2
            
        if t > (math.pi)/4 and t < ((math.pi)/4)*3:   
            msg.linear.x = 0     
            msg.angular.z = 0

        if t >= ((math.pi)*3/4) and t < ((math.pi)*5/4):
            a = (math.sqrt(2*math.cos(2*t))) * (math.cos(t))

            b = math.sqrt(2*math.cos(2*t)) * (math.sin(t))
            
            k = 3*(math.sqrt(a**2+b**2))
            c = float(a*2)
            d = float(b*2)
            msg.linear.x = 1.2       
            msg.angular.z = k*1.2       

        if t > ((math.pi)/4)*5 and t < ((math.pi)/4)*7:
            msg.linear.x = 0     
            msg.angular.z = 0
        
        if t >= ((math.pi)/4)*7 and t < 2*(math.pi):
            a = math.sqrt(2*math.cos(2*t)) * (math.cos(t))
            b = ((math.sqrt(2*math.cos(2*t)) * (math.sin(t))))
            
            k = 3*(math.sqrt(a**2+b**2))
            c = float(a*3)
            d = float(b*3)
            msg.linear.x = 1.2       
            msg.angular.z = k*1.2       


        #k = 3*(math.sqrt(a**2+b**2))

        # c = float(a*2)
        # d = float(b*2)
        # msg.linear.x = 1.2  
        # msg.angular.z = k*1.2
        i += 1

        pub.publish(msg)
        
        
        
        rate.sleep()
