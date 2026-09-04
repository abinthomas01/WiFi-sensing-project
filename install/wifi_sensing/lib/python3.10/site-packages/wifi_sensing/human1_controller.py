import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SetEntityState
from wifi_sensing.waypoints import WAYPOINTS

class HumanMover(Node):
    def __init__(self):
        super().__init__('human_mover')
        self.client = self.create_client(SetEntityState, '/gazebo/set_entity_state')
        
        # Wait for Gazebo to be ready
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Gazebo /set_entity_state service...')
        
        # IMPORTANT: Change this if your model has a different name in Gazebo!
        self.model_name = "middle_age_man__rigged__animated__free" 
        
        self.current_index = 0
        self.total_waypoints = len(WAYPOINTS)
        
        # Create a timer that moves the model every 2 seconds
        self.timer = self.create_timer(2.0, self.move_to_next_waypoint)
        self.get_logger().info('Human Mover Node Started! Moving in 2 seconds...')

    def move_to_next_waypoint(self):
        if self.current_index >= self.total_waypoints:
            self.get_logger().info('Reached the end of the route! Stopping.')
            self.timer.cancel()
            return

        # Get the next coordinate
        x, y, z = WAYPOINTS[self.current_index]

        # Create the request
        req = SetEntityState.Request()
        req.state.name = self.model_name
        req.state.pose.position.x = float(x)
        req.state.pose.position.y = float(y)
        req.state.pose.position.z = float(z)
        
        # Keep the model standing upright (no rotation)
        req.state.pose.orientation.w = 1.0 

        self.get_logger().info(f'Moving {self.model_name} to Waypoint {self.current_index + 1}: X={x}, Y={y}, Z={z}')
        self.client.call_async(req)

        # Move to the next waypoint for the next timer tick
        self.current_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = HumanMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
