"""
PyBullet DIRECT(헤드리스) 모드 — 창 없이 물리 시뮬레이션 후 카메라 이미지 캡처.
Docker 컨테이너나 SSH 세션에서도 돌아갑니다.

실행:
    pip install pybullet numpy pillow
    python headless_capture.py     # 결과: ./panda_capture.png
"""

import numpy as np
import pybullet as p
import pybullet_data
from PIL import Image


def main() -> None:
    p.connect(p.DIRECT)
    p.setGravity(0, 0, -9.81)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")
    p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

    for _ in range(240):  # 1 초 안정화
        p.stepSimulation()

    width, height = 640, 480
    view = p.computeViewMatrix(
        cameraEyePosition=[1.2, 1.2, 1.0],
        cameraTargetPosition=[0, 0, 0.3],
        cameraUpVector=[0, 0, 1],
    )
    proj = p.computeProjectionMatrixFOV(
        fov=60, aspect=width / height, nearVal=0.1, farVal=10
    )
    img = p.getCameraImage(
        width, height, view, proj, renderer=p.ER_BULLET_HARDWARE_OPENGL
    )
    rgb = np.reshape(img[2], (height, width, 4))[:, :, :3].astype(np.uint8)
    Image.fromarray(rgb).save("panda_capture.png")
    print("saved: panda_capture.png")

    p.disconnect()


if __name__ == "__main__":
    main()
