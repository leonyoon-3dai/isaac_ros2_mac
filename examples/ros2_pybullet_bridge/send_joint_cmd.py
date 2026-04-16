"""
Docker ROS 2 컨테이너 안에서 /joint_cmd 로 테스트 커맨드 전송.

실행 (컨테이너 안에서):
    pip install rclpy  # 이미지에 따라 이미 설치됨
    python send_joint_cmd.py
"""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointCommander(Node):
    def __init__(self) -> None:
        super().__init__("joint_commander")
        self.pub = self.create_publisher(JointState, "/joint_cmd", 10)
        self.t = 0.0
        self.create_timer(0.05, self.tick)

    def tick(self) -> None:
        self.t += 0.05
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [f"panda_joint{i+1}" for i in range(7)]
        js.position = [
            0.5 * math.sin(self.t),
            -0.5 + 0.2 * math.sin(self.t),
            0.0,
            -2.0 + 0.3 * math.sin(self.t),
            0.0,
            1.5,
            0.7,
        ]
        self.pub.publish(js)


def main() -> None:
    rclpy.init()
    try:
        rclpy.spin(JointCommander())
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == "__main__":
    main()
