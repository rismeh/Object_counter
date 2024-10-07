# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import LaserScan
from std_msgs.msg import UInt8

#import requiered data types



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('object_detection')
        self.subscription = self.create_subscription(LaserScan, '/dolly/laser_scan', self.callbackLaser, 10)
        self.publisher_ = self.create_publisher(UInt8, 'number_objects', 1)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.subscription  # prevent unused variable warning
    
    def timer_callback(self):
        self.i += 1

    def callbackLaser(self, data):
        #create an array of measurement angles (complete here)
        self.get_logger().info('Angle measurment : "%s"' % data.angle_increment)
        self.angles = np.array(data.angle_increment)
        self.get_logger().info('Angle maximum : "%s"' % data.angle_max)
        self.angle_max = np.array(data.angle_max) 
        self.get_logger().info('Angle minimum : "%s"' % data.angle_min)
        self.angle_min = np.array(data.angle_min)
      
        #extract from data the max measured range (complete here)
        self.get_logger().info('Maximum range measurment : "%s"' % data.range_max)
        self.range_max = np.array(data.range_max)
        self.get_logger().info('Minimum range measurment : "%s"' % data.range_min)
        self.range_min = np.array(data.range_min)
        self.max_valid_distance = data.range_max
        self.get_logger().info('Ranges : "%s"' % data.ranges)
        self.range_max_valid = np.array(data.ranges)
       

        #call function/service for detecting objects
        nO = self.getNumberObjects(data.ranges)
        self.nObjects = UInt8()
        self.nObjects.data = nO

        #write number of objects as log
        self.get_logger().info('number of detected objects : %s ' % (nO))
        
        #publish number of obects
        self.publisher_.publish(self.nObjects)

        #log distances and angles
    
           # self.get_logger().info('data %d: angle[%f] data[%f]' % (i, self.angles[i], data.ranges[i]))
    
    def getNumberObjects(self, ranges):
        #function for getting number of detected objects (complete here)
        nObjects = 0
        for i in range(0, np.size(ranges)):
            dist = ranges[i] - ranges[i-1]
            if abs(dist) > 1 and ranges[i] < self.max_valid_distance:
                nObjects += 1
        return nObjects 
            
        

def main(args=None):
    rclpy.init(args=args)

    object_detector= MinimalSubscriber()

    rclpy.spin(object_detector)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    object_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
