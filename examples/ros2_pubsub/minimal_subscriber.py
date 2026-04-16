"""
ROS 2 Jazzy 최소 subscriber 예제. `chatter` 토픽을 듣는다.

사용 방법:
    `ros2 run my_py_pkg subscriber`
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("minimal_subscriber")
        self.subscription = self.create_subscription(
            String, "chatter", self.listener_callback, 10
        )

    def listener_callback(self, msg: String):
        self.get_logger().info(f"받음: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
