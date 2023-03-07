import Lidar
import IMU

from Movement_Threshold import Movement_Threshold
import numpy as np
import utils

class Sensors:

    def __init__(self):
        self.lidar = Lidar(self)
        self.imu = IMU(self)
        self.lidar_pose = None
        self.thresholds = []

    def init_lidar(self):
        self.lidar.wait_for_pose_set()

    def init_imu(self):
        pass
    
    def callback_lidar_pose(self, pose):
        self.lidar_pose = pose
        self.check_threshold()

    def check_thresholds(self):
        for i in range(len(self.thresholds) - 1, -1, -1): # Gotta iterate backwards as stuff might get removed from the list
            t = self.thresholds[i]
            triggered = t.axis_func(self.lidar_pose, t)
            if triggered:
                self.thresholds.pop(i)
                t.function() # run the lamba associated with the threshold

    def add_listener(self, threshold):
        self.thresholds.append(threshold)

    def remove_listeners(self, tag):
        """
            Removes all listeners with the given tag
        """
        for i in range(len(self.thresholds) - 1, -1, -1):
            if self.thresholds[i].tag == tag:
                self.thresholds.pop(i)

    def get_lidar_pose(self):
        return self.lidar.get_pose()
    
    def get_obstacle_points(self):
        return self.lidar.prepare_obstacle_points()
    
    def get_movement_points(self, points_list):
        return self.lidar.prepare_movement_points(points_list)