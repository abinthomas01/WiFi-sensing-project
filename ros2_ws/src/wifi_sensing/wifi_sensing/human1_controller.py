import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SetEntityState
from wifi_sensing.waypoints import WAYPOINTS
import math

class HumanSlider(Node):
    def __init__(self):
        super().__init__('human_slider')
        self.client = self.create_client(SetEntityState, '/gazebo/set_entity_state')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Gazebo /set_entity_state service...')
        
        self.model_name = "the_strangler"
        self.current_index = 0
        
        self.current_x = float(WAYPOINTS[0][0])
        self.current_y = float(WAYPOINTS[0][1])
        self.speed = 0.05 
        
        self.timer = self.create_timer(0.1, self.move_smoothly)
        self.get_logger().info('Strangler Slider Started!')

    def move_smoothly(self):
        if self.current_index >= len(WAYPOINTS) - 1:
            self.get_logger().info('Reached the end of the route! Stopping.')
            self.timer.cancel()
            return

        target_x = float(WAYPOINTS[self.current_index + 1][0])
        target_y = float(WAYPOINTS[self.current_index + 1][1])

        dx = target_x - self.current_x
        dy = target_y - self.current_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.current_x = target_x
            self.current_y = target_y
            self.current_index += 1
            self.get_logger().info(f'Reached Waypoint {self.current_index + 1}')
        else:
            self.current_x += (dx / distance) * self.speed
            self.current_y += (dy / distance) * self.speed

        req = SetEntityState.Request()
        req.state.name = self.model_name
        req.state.pose.position.x = self.current_x
        req.state.pose.position.y = self.current_y
        req.state.pose.position.z = 0.0
        
        angle = math.atan2(dy, dx)
        req.state.pose.orientation.z = math.sin(angle / 2.0)
        req.state.pose.orientation.w = math.cos(angle / 2.0)

        self.client.call_async(req)

def main(args=None):
    rclpy.init(args=args)
    node = HumanSlider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()