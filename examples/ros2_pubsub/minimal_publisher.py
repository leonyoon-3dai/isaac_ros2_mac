"""
ROS 2 Jazzy 최소 publisher 예제 (Docker 컨테이너 안에서 실행).

사용 방법:
    1) Docker ROS 2 컨테이너 안에서
       `cd /root/ros2_ws/src/my_py_pkg/my_py_pkg/` 에 이 파일을 둔다.
    2) `colcon build --packages-select my_py_pkg`
    3) `source install/setup.bash`
    4) `ros2 run my_py_pkg publisher`
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__("minimal_publisher")
        self.publisher_ = self.create_publisher(String, "chatter", 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f"안녕 ROS 2 from Intel Mac! #{self.i}"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publish: {msg.data}")
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
