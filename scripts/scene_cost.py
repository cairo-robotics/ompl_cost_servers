#!/usr/bin/env python

from moveit_msgs.srv import CustomCost, CustomCostResponse
from moveit_msgs.msg import PlanningScene
import rospy

# Global obstacles object that will be updated
# by subscribing to the ROS stack
obstacles = []


def handle_scene_based_cost(request):
    # TODO: Compute cost according to the scene that is read
    cost = 0.1
    srv = CustomCostResponse()
    srv.cost = cost
    srv.type = 0
    return srv


def handle_scene_callback(message):
    # Create obstacle objects from scene data
    obstacles = [
        Obstacle() for i in range(len(message.world.collision_objects))]
    for c_o, ob in zip(message.world.collision_objects, obstacles):
        #  Set ID
        ob.id = c_o.id

        # Setup primatives
        for p in c_o.primitives:
            ob.primitives.append(p.dimensions)

        # Setup primative poses
        for p in c_o.primitive_poses:
            ob.primitive_poses.append({
                    'position': p.position,
                    'orientation': p.orientation
                })

    # Print Obstacles
    print("Found obstacles in scene:")
    for ob in obstacles:
        ob.print_data()
        print("---")


def scene_cost_server():
    # Setup cost server
    rospy.init_node('scene_cost_server')
    rospy.Service('custom_cost', CustomCost, handle_scene_based_cost)

    # Subscribe to planning scene for obstacle data
    rospy.Subscriber("/planning_scene", PlanningScene, handle_scene_callback)

    # Wait for service calls
    rospy.loginfo("Ready to read scene for eventual cost computation.")
    rospy.spin()


class Obstacle:
    def __init__(self):
        self.id = ""
        self.primitives = []
        self.primitive_poses = []

    def print_data(self):
        rospy.loginfo("ID: %s" % self.id)
        rospy.loginfo("Dimensions: %s" % str(self.primitives[0]))
        rospy.loginfo("Position: %s" % repr(
            self.primitive_poses[0]['position']))
        rospy.loginfo("Orientation: %s" % repr(
            self.primitive_poses[0]['orientation']))


if __name__ == "__main__":
    scene_cost_server()
