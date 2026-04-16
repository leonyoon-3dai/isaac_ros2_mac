"""
"작은 Isaac Sim" — ROS 2 ↔ PyBullet 브리지.

구조:
    /joint_cmd    (subscribe, sensor_msgs/JointState)   →   PyBullet setJointMotorControl2
    /joint_states (publish,   sensor_msgs/JointState)  ←   PyBullet getJointState

실행:
    # ROS 2 rclpy 를 Mac 네이티브 venv 에서 얻어오는 커뮤니티 경로:
    pip install catkin_pkg empy==3.3.4 lark numpy
    pip install --extra-index-url https://rospypi.github.io/simple/ rclpy sensor_msgs std_msgs
    pip install pybullet
    python sim_bridge.py

주의:
    rospypi 배포는 비공식이고 플랫폼 지원이 제한적일 수 있습니다.
    안정성이 필요하면 Docker ROS 2 컨테이너 안에 브리지 전체를 옮기고
    PyBullet 은 `p.DIRECT` 헤드리스로 돌리세요.
"""

from __future__ import annotations

import pybullet as p
import pybullet_data
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class PandaSimBridge(Node):
    NUM_ARM_JOINTS = 7

    def __init__(self) -> None:
        super().__init__("panda_sim_bridge")

        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        self.robot = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        self.create_subscription(JointState, "/joint_cmd", self.cmd_cb, 10)
        self.create_timer(1.0 / 240.0, self.step)

        self.get_logger().info("PandaSimBridge ready. topics: /joint_cmd, /joint_states")

    def cmd_cb(self, msg: JointState) -> None:
        for i, pos in enumerate(msg.position[: self.NUM_ARM_JOINTS]):
            p.setJointMotorControl2(
                self.robot, i, p.POSITION_CONTROL, targetPosition=pos, force=87.0
            )

    def step(self) -> None:
        p.stepSimulation()
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [f"panda_joint{i+1}" for i in range(self.NUM_ARM_JOINTS)]
        js.position = [
            p.getJointState(self.robot, i)[0] for i in range(self.NUM_ARM_JOINTS)
        ]
        js.velocity = [
            p.getJointState(self.robot, i)[1] for i in range(self.NUM_ARM_JOINTS)
        ]
        self.pub.publish(js)


def main() -> None:
    rclpy.init()
    node = PandaSimBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
