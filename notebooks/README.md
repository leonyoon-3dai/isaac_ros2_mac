# notebooks/ — Google Colab 노트북

Intel Mac 에 로컬 환경을 전혀 세팅하지 않고도 브라우저만으로 Isaac Sim 의 핵심 개념을 체험할 수 있도록 설계된 한국어 Colab 노트북 3종.

| # | 노트북 | 주제 | 열어보기 |
|---|--------|------|----------|
| 01 | [01_pybullet_panda.ipynb](01_pybullet_panda.ipynb) | PyBullet 로 Franka Panda 팔 로드·제어·IK·렌더 → GIF·플롯 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/01_pybullet_panda.ipynb) |
| 02 | [02_ros2_rclpy.ipynb](02_ros2_rclpy.ipynb) | Colab 에 ROS 2 Humble 설치, Python pub/sub, 토픽 데이터 시각화 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/02_ros2_rclpy.ipynb) |
| 03 | [03_ros2_pybullet_bridge.ipynb](03_ros2_pybullet_bridge.ipynb) | ROS 2 ↔ PyBullet 브리지로 "작은 Isaac Sim" — 명령/실측 플롯 + 카메라 GIF | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/03_ros2_pybullet_bridge.ipynb) |

## 실행 팁

1. Colab 탭 열기 → `런타임 → 런타임 유형 변경` → **CPU 로 충분** (GPU 선택은 자유). 이 튜토리얼은 CPU 만으로 전부 돌아갑니다.
2. 첫 셀(설치) 는 런타임당 **1회** 만 실행하면 됩니다 (약 2~3분).
3. 02/03 번 노트북은 ROS 2 Humble 을 apt 로 설치합니다. Colab 의 sudo 권한은 자동으로 허용됩니다.
4. 노트북 시각화가 끊어지면 `런타임 → 다시 시작 및 모두 실행` 을 눌러 보세요.

## Mac 로컬 실행 vs Colab 차이

| | Mac 로컬 (`examples/`) | Colab (`notebooks/`) |
|---|---|---|
| ROS 2 배포판 | Jazzy (Docker `osrf/ros`) | Humble (apt) |
| PyBullet 모드 | `p.GUI` 창 직접 | `p.DIRECT` + GIF/PNG |
| GUI 가능 | XQuartz 로 turtlesim/RViz | ❌ (브라우저 출력만) |
| 주 용도 | 상시 개발, 디버깅 | 학습·공유·시각적 시연 |

ROS 2 Humble 과 Jazzy 는 **API 가 대부분 호환** 됩니다. 이 노트북들에서 쓴 rclpy/Python 코드는 Docker Jazzy 컨테이너에서도 **그대로 실행**됩니다.
