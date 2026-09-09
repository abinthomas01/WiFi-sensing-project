import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SetEntityState
import math

# 1. Define the routes directly in the code so it's easy to see
STRANGLER_ROUTE = [
    [1.67597, 1.00138], #hall
    [4.80501, 1.95532],   # Room 2
    [-2.01522, -2.00758],  # Room 3
    [1.67597, 1.00138], #hall
]

WOMAN_ROUTE = [
    [-1.69931, 2.28462],  # Kitchen
    [1.67597, 1.00138],   # Hall
    [-2.44060, -0.072066], # Bathroom
    [1.67597, 1.00138],   # Hall
    [-1.69931, 2.28462],  # Kitchen
]

MAN_ROUTE = [
    [-2.01522, -2.00758], # Room 3
    [1.67597, 1.00138], #hall
    [-1.69931, 2.28462],  # Kitchen
    [4.98137, -0.005603],  # Room 1
    [1.67597, 1.00138], #hall
    [-2.01522, -2.00758], # Room 3
]

# Girl: Bathroom -> Room 2 -> Kitchen
GIRL_ROUTE = [
    [-2.44060, -0.072066], # Bathroom
    [4.80501, 1.95532],    # Room 2
    [1.67597, 1.00138],   # Hall
    [-1.69931, 2.28462],    # Kitchen
    [1.67597, 1.00138], #hall
    [-2.44060, -0.072066], # Bathroom
]

# Balthazar: Room 1 -> Hall -> Kitchen
BALTHAZAR_ROUTE = [
    [4.98137, -0.005603],  # Room 1
    [1.67597, 1.00138],    # Hall
    [-1.69931, 2.28462]    # Kitchen
]

# 2. This is the exact same sliding logic we used before
class SliderBrain:
    def __init__(self, node, model_name, waypoints):
        self.model_name = model_name
        self.waypoints = waypoints
        self.client = node.create_client(SetEntityState, '/gazebo/set_entity_state')
        
        self.current_index = 0
        self.current_x = float(self.waypoints[0][0])
        self.current_y = float(self.waypoints[0][1])
        self.speed = 0.05 
        
        # Create a timer for this specific model
        self.timer = node.create_timer(0.1, self.move_smoothly)
        node.get_logger().info(f'{self.model_name} started moving!')

    def move_smoothly(self):
        # If we reach the end of the route, loop back to the beginning (-1)
        # So the next target becomes waypoints[0]
        if self.current_index >= len(self.waypoints) - 1:
            self.current_index = -1

        target_x = float(self.waypoints[self.current_index + 1][0])
        target_y = float(self.waypoints[self.current_index + 1][1])

        dx = target_x - self.current_x
        dy = target_y - self.current_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.current_x = target_x
            self.current_y = target_y
            self.current_index += 1
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

# 3. The main node that holds both brains
class DualHumanSlider(Node):
    def __init__(self):
        super().__init__('dual_human_slider')
        
        # Wait for Gazebo to be ready
        self.client = self.create_client(SetEntityState, '/gazebo/set_entity_state')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Gazebo /set_entity_state service...')

        # Create the Strangler brain
        self.strangler = SliderBrain(self, "the_strangler", STRANGLER_ROUTE)
        
        # Create the Woman brain
        self.woman = SliderBrain(self, "realistic_woman_walking_animated_1", WOMAN_ROUTE)

        # Create the Man brain
        self.man = SliderBrain(self, "middle_age_man__rigged__animated__free", MAN_ROUTE)

        # Create the Girl brain
        self.girl = SliderBrain(self, "girl_with_clothes", GIRL_ROUTE)

        # Create the Blathazar brain
        self.balthazar = SliderBrain(self, "balthazar_rigged_animated", BALTHAZAR_ROUTE)

def main(args=None):
    rclpy.init(args=args)
    node = DualHumanSlider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()