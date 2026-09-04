import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/abin/Projects/wifi_sensing_ros2/install/wifi_sensing'
