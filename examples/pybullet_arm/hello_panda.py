"""
PyBullet Hello World: Franka Panda 팔을 불러와 중력에 떨어뜨리고 단일 목표각으로 제어.

사전 요구:
    source ~/venvs/robotics/bin/activate
    pip install pybullet numpy

실행:
    python hello_panda.py

GPU 불필요 — Intel Iris Plus Graphics 640 에서도 충분히 동작합니다.
"""

import time

import pybullet as p
import pybullet_data


def main(duration_sec: float = 5.0, dt: float = 1.0 / 240.0) -> None:
    # 1) 시뮬레이터 연결 (GUI 모드)
    client = p.connect(p.GUI)
    p.setGravity(0, 0, -9.81, physicsClientId=client)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # 2) 바닥과 로봇 로드
    p.loadURDF("plane.urdf")
    robot = p.loadURDF(
        "franka_panda/panda.urdf",
        basePosition=[0, 0, 0],
        useFixedBase=True,
    )

    # 3) 7 개 팔 관절에 목표 각도 지정
    target = [0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.7]
    for i, angle in enumerate(target):
        p.setJointMotorControl2(
            robot,
            jointIndex=i,
            controlMode=p.POSITION_CONTROL,
            targetPosition=angle,
            force=87.0,  # Panda 데이터시트 상 조인트 토크 한계(예시값)
        )

    # 4) 고정 시간만큼 시뮬레이션
    n_steps = int(duration_sec / dt)
    for _ in range(n_steps):
        p.stepSimulation()
        time.sleep(dt)

    p.disconnect()


if __name__ == "__main__":
    main()
