# Isaac Sim + ROS 2 on Intel Mac (GPU 없음) — 한국어 초심자 튜토리얼

> **타깃 하드웨어**: MacBook Pro 2017 13" (Intel i7 · 16GB · Intel Iris Plus 640 · macOS 13.7.8 Ventura)
> **목표**: NVIDIA GPU 가 없는 Intel Mac 에서 Isaac Sim 과 ROS 2 의 세계에 **Python 레벨로** 발을 들이는 가장 쉬운 길을 단계적으로 보여준다.

이 환경은 "Isaac Sim 을 로컬에서 네이티브로 돌리는 것" 은 **불가능** 합니다. 그러나 Python 레벨 ROS 2 + 물리 시뮬레이션 + 클라우드 Isaac Sim 세 경로로 **실질적으로 같은 학습 효과** 를 얻을 수 있습니다. 이 리포는 각 경로를 친절하게 풀어 설명하는 한국어 튜토리얼입니다.

---

## 📚 파일 안내

| 파일 | 내용 |
|------|------|
| [`TUTORIAL_KR.md`](TUTORIAL_KR.md) | 본편 — 환경 점검부터 ROS 2 Docker, PyBullet, 클라우드 Isaac Sim, 통합 예제까지 |
| [`notebooks/`](notebooks/) | **Google Colab 노트북 3종** (설치 제로, 브라우저만으로 체험) |
| [`examples/ros2_pubsub/`](examples/ros2_pubsub/) | 최소 Python ROS 2 publisher/subscriber 쌍 |
| [`examples/pybullet_arm/`](examples/pybullet_arm/) | Franka Panda 팔을 PyBullet 으로 로드하는 최소 스크립트 |
| [`examples/ros2_pybullet_bridge/`](examples/ros2_pybullet_bridge/) | ROS 2 토픽 ↔ PyBullet 시뮬레이션 브리지 데모 |

### 🚀 Google Colab 바로 열기

| # | 주제 | Colab |
|---|------|-------|
| 01 | **PyBullet Panda** — GIF 애니메이션 + IK + 관절 궤적 플롯 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/01_pybullet_panda.ipynb) |
| 02 | **ROS 2 rclpy** — Humble 설치 + pub/sub + 토픽 시각화 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/02_ros2_rclpy.ipynb) |
| 03 | **ROS 2 × PyBullet 브리지** — 명령/실측 비교 + 카메라 GIF | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/leonyoon-3dai/isaac_ros2_mac/blob/main/notebooks/03_ros2_pybullet_bridge.ipynb) |

> 💡 Colab 은 Ubuntu 22.04 + GPU(옵션) 환경이라 **설치 제로** 로 ROS 2 + PyBullet 을 바로 써 볼 수 있습니다. Mac 로컬 세팅 없이 개념부터 체험하고 싶을 때 최적.

## 🎯 60초 요약

```
┌─────────────────────────────────────────────────────────────────┐
│  Intel Mac + GPU 없음 에서 "할 수 있는 것 / 못 하는 것"             │
├─────────────────────────────────────────────────────────────────┤
│  ✅ ROS 2 Jazzy (Docker)       : 쉽고 빠름, x86_64 네이티브       │
│  ✅ PyBullet / MuJoCo          : pip 한 줄, GPU 불필요             │
│  ✅ Gazebo Harmonic (Docker)   : ROS 2 Docker 안에서               │
│  ✅ Isaac Sim (클라우드)         : 브라우저로 원격 접속 (NVIDIA Brev) │
│  ❌ Isaac Sim 로컬 네이티브      : NVIDIA GPU 필수, 불가능          │
│  ❌ Omniverse Kit 로컬          : RTX GPU 필수                     │
│  ❌ CUDA/cuDNN 로컬             : NVIDIA GPU 필요                   │
└─────────────────────────────────────────────────────────────────┘
```

**추천 학습 순서** (이 리포의 TUTORIAL_KR.md 구성과 동일):

1. **ROS 2 를 Docker 로 실행** → turtlesim 으로 기본 개념 체득
2. **Python 으로 publisher/subscriber 작성** → rclpy 맛보기
3. **PyBullet 로 순수 Python 물리 시뮬레이션** → 로봇 팔 로드·제어
4. **ROS 2 ↔ PyBullet 브리지** → Isaac Sim 이 하는 일의 핵심 구조 이해
5. **필요하면** NVIDIA Brev 로 클라우드 Isaac Sim 접속

상세 내용은 **[TUTORIAL_KR.md](TUTORIAL_KR.md)** 로 가세요.

---

## ⚠️ 면책

- 본 리포는 NVIDIA 공식 자료가 아닌 개인 학습용 비공식 요약입니다.
- 모든 스크린샷/다이어그램은 각 프로젝트의 공식 문서·위키피디아·아이콘 CDN 을 인용합니다.
- 기준일: **2026-04-17** · ROS 2 Jazzy, Gazebo Harmonic, Isaac Sim 5.x 시점.
