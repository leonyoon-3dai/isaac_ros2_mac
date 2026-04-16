# Intel Mac(GPU 없음)에서 Isaac Sim · ROS 2 입문 — 한국어 튜토리얼

> 2017년형 MacBook Pro 13"(Intel i7 + Intel Iris Plus 640, macOS Ventura 13.7.8, 16 GB RAM) 를 실제 타깃으로 잡은 초심자 가이드. Python 레벨만 이해해도 따라갈 수 있도록, 모든 단계를 복붙 가능한 터미널 명령으로 제공합니다.

## 목차

- [0. 시작 전 — 솔직한 현실 체크](#0-시작-전--솔직한-현실-체크)
- [1. 공통 준비물 (Homebrew · XQuartz · Docker · Python)](#1-공통-준비물-homebrew--xquartz--docker--python)
- [2. Track A — ROS 2 Jazzy를 Docker로 실행하기](#2-track-a--ros-2-jazzy를-docker로-실행하기)
- [3. Track A 실습 — turtlesim 움직여 보기](#3-track-a-실습--turtlesim-움직여-보기)
- [4. rclpy 로 내 첫 Python 노드 만들기](#4-rclpy-로-내-첫-python-노드-만들기)
- [5. Track B — PyBullet 로 GPU 없이 로봇 팔 굴리기](#5-track-b--pybullet-로-gpu-없이-로봇-팔-굴리기)
- [6. ROS 2 ↔ PyBullet 브리지 — "작은 Isaac Sim" 만들기](#6-ros-2--pybullet-브리지--작은-isaac-sim-만들기)
- [7. Track C — 클라우드로 진짜 Isaac Sim 써 보기 (NVIDIA Brev)](#7-track-c--클라우드로-진짜-isaac-sim-써-보기-nvidia-brev)
- [8. 다음 단계 — 추천 학습 로드맵](#8-다음-단계--추천-학습-로드맵)
- [9. 트러블슈팅 FAQ](#9-트러블슈팅-faq)
- [10. 참고 자료](#10-참고-자료)

---

## 0. 시작 전 — 솔직한 현실 체크

### 0.1 Isaac Sim 은 내 Mac 에서 네이티브로 돌까요?

> ❌ **안 됩니다.**
> Isaac Sim / Omniverse Kit 은 **NVIDIA RTX GPU + Linux/Windows x86_64** 전용입니다. macOS 바이너리 자체가 없고, GPU 가 있어도 Mac 은 CUDA 를 지원하지 않습니다.
> — [Isaac Sim 시스템 요구사항 (공식 문서)](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html)

### 0.2 그럼 뭘로 공부하나요?

Isaac Sim 의 "본질" 은 결국 **로봇 파라미터(URDF/USD) → 물리 엔진 → 센서 렌더링 → Python API** 입니다. 이 파이프라인은 아래 조합으로 **GPU 없이** 구현할 수 있습니다.

| 구성 요소 | Isaac Sim | Intel Mac 대체 |
|-----------|-----------|----------------|
| 물리 엔진 | NVIDIA PhysX (GPU) | **PyBullet** (CPU) 또는 **MuJoCo** (CPU) |
| 로봇 설명 | USD / URDF | **URDF** 공통 |
| 센서 렌더 | RTX ray tracing | PyBullet OpenGL / DIRECT mode (headless) |
| Python API | `omni.isaac.*` | **`pybullet`**, **`mujoco`**, **`rclpy`** |
| 로봇 미들웨어 | Isaac Sim ROS 브리지 | **ROS 2 Jazzy (Docker)** |

### 0.3 Isaac Sim "그 자체" 를 꼭 만져야 한다면

- ✅ [**NVIDIA Brev Launchable**](https://github.com/isaac-sim/isaac-launchable) — 클릭 한 번으로 클라우드 GPU 인스턴스에 Isaac Sim + Isaac Lab + VS Code 띄움, **브라우저** 로 접속 → Intel Mac 에서 완전히 작동.
- ⚠️ Isaac Sim WebRTC Streaming Client 네이티브 앱 — macOS 용은 존재하지만 Apple Silicon 에서는 오류 보고 다수, Intel Mac 호환성은 케이스별.

---

## 1. 공통 준비물 (Homebrew · XQuartz · Docker · Python)

### 1.1 Homebrew 설치 (아직 없다면)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치 후 PATH 업데이트:

```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

> 💡 Intel Mac 의 Homebrew 루트는 `/usr/local`, Apple Silicon 은 `/opt/homebrew` 입니다. 이 가이드는 Intel 경로를 씁니다.

### 1.2 Docker Desktop 설치

[Docker Desktop for Mac — Intel chip 다운로드](https://desktop.docker.com/mac/main/amd64/Docker.dmg) → 설치 후 실행 → 메뉴 막대에 🐳 고래 아이콘 확인.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Docker_%28container_engine%29_logo.svg/320px-Docker_%28container_engine%29_logo.svg.png" width="160" alt="Docker logo">
</p>

설정 > Resources > CPU 4개, Memory 6~8GB 로 올려두면 ROS 2 빌드가 한결 편합니다.

**동작 확인**:

```bash
docker run --rm hello-world
```

`Hello from Docker!` 출력이 보이면 OK.

> 🟢 **Intel Mac 의 장점**: 이 기기는 x86_64 이므로 ROS 2 Docker 이미지(공식 `linux/amd64`) 를 **QEMU 에뮬레이션 없이** 바로 돌립니다. Apple Silicon 대비 훨씬 빠릅니다.

### 1.3 XQuartz 설치 (GUI 앱용 X11 서버)

turtlesim·RViz 같은 GUI 도구를 Docker 컨테이너 안에서 띄우려면 Mac 쪽에 X11 서버가 필요합니다.

```bash
brew install --cask xquartz
```

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/XQuartz_logo.svg/240px-XQuartz_logo.svg.png" width="120" alt="XQuartz logo">
</p>

설치 후 **반드시 로그아웃 → 다시 로그인** 또는 재부팅. 그 다음:

1. XQuartz 실행 → 메뉴 `XQuartz → Settings…` (또는 Preferences)
2. **Security 탭** → `Allow connections from network clients` **체크**
3. XQuartz 를 **완전히 종료** 후 재실행 (설정 적용)

터미널에서 한 줄:

```bash
# 로컬호스트에서 오는 X11 연결 허용
xhost + 127.0.0.1
```

### 1.4 Python 준비

macOS 의 시스템 Python 말고, 별도 버전을 쓰는 걸 권장합니다.

```bash
brew install python@3.11
python3.11 -m venv ~/venvs/robotics
source ~/venvs/robotics/bin/activate
pip install --upgrade pip
```

이후 이 튜토리얼의 Python 은 전부 이 `~/venvs/robotics` 가상환경 기준입니다.

---

## 2. Track A — ROS 2 Jazzy를 Docker로 실행하기

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/b/bb/Ros_logo.svg" width="200" alt="ROS logo">
</p>

ROS 2 (Robot Operating System 2) 는 로봇용 **메시지 기반 분산 시스템** 이에요. "노드(Node)가 토픽(Topic)에 메시지(Message)를 publish/subscribe 한다" 가 핵심.

### 2.1 왜 Docker 인가?

| 옵션 | 난이도 | 성능 | 이 Mac 에 적합? |
|------|-------|------|------------------|
| 소스 빌드 (brew + venv) | 😓 매우 높음 | 네이티브 | Ventura 에서 가능하지만 시행착오 많음 |
| **Docker (공식 `osrf/ros`)** | 😌 낮음 | **x86_64 네이티브** (Intel Mac!) | ✅ **강력 추천** |
| VM (VirtualBox/UTM) | 😐 중간 | 에뮬레이션 | 오버헤드 큼 |

### 2.2 ROS 2 Jazzy 이미지 가져오기

ROS 2 공식 이미지 태그 (Docker Hub `osrf/ros`):

| 태그 | 내용 |
|------|------|
| `jazzy-ros-core` | 최소 베이스 (CLI 툴 일부) |
| `jazzy-ros-base` | 빌드 도구·`colcon` 포함 |
| **`jazzy-desktop`** | **RViz2, rqt, turtlesim 포함 ← 이 튜토리얼용** |
| `jazzy-desktop-full` | 데스크탑 + 시뮬레이터 패키지 |

```bash
docker pull osrf/ros:jazzy-desktop
```

> 📦 약 2.5 GB. 다운로드에 10~15분 걸릴 수 있어요.

### 2.3 워크스페이스 폴더 만들기

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### 2.4 컨테이너 실행 (GUI 포함)

```bash
# XQuartz 허용 (한 세션당 1회)
xhost + 127.0.0.1

docker run -it --rm \
  --name ros2 \
  -e DISPLAY=host.docker.internal:0 \
  -v ~/ros2_ws:/root/ros2_ws \
  osrf/ros:jazzy-desktop \
  bash
```

명령어 해설:
- `--rm` : 컨테이너 종료 시 자동 삭제
- `-e DISPLAY=host.docker.internal:0` : 컨테이너 내부 앱이 Mac 의 XQuartz(:0) 로 그림 출력
- `-v ~/ros2_ws:/root/ros2_ws` : Mac 쪽 `~/ros2_ws` 를 컨테이너의 `/root/ros2_ws` 와 공유 (실시간 동기화)

컨테이너 안 프롬프트가 `root@…:/#` 로 바뀌면 성공.

### 2.5 매번 반복할 세팅 스크립트

컨테이너 안에서:

```bash
source /opt/ros/jazzy/setup.bash
echo $ROS_DISTRO   # jazzy
ros2 --help        # 명령 목록 확인
```

매번 치기 귀찮다면 `.bashrc` 에 추가:
```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

---

## 3. Track A 실습 — turtlesim 움직여 보기

<p align="center">
  <img src="https://docs.ros.org/en/jazzy/_images/turtlesim.png" width="360" alt="turtlesim screenshot">
</p>

> 🐢 **turtlesim** 은 ROS 의 "Hello World". 2D 화면 위 거북이를 토픽으로 움직여 publisher/subscriber 개념을 체득합니다.

### 3.1 거북이 창 띄우기

**컨테이너 안 터미널 1** 에서:

```bash
ros2 run turtlesim turtlesim_node
```

Mac XQuartz 쪽에서 거북이 창이 뜨면 성공.
(뜨지 않으면 [트러블슈팅 9.2](#92-gui-창이-안-떠요-xquartz))

### 3.2 거북이 조종

**컨테이너에 두 번째 터미널로 접속** (Mac 새 탭):

```bash
docker exec -it ros2 bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtle_teleop_key
```

키보드 방향키로 거북이를 움직여 봅니다.

### 3.3 토픽 들여다보기

**터미널 3**:

```bash
docker exec -it ros2 bash
source /opt/ros/jazzy/setup.bash
ros2 topic list
ros2 topic echo /turtle1/pose
```

움직일 때마다 좌표·속도 메시지가 흘러나오는 게 보입니다. 이게 바로 ROS 의 **pub/sub 통신**.

### 3.4 시각적 구조 파악 — rqt_graph

```bash
ros2 run rqt_graph rqt_graph
```

<p align="center">
  <img src="https://docs.ros.org/en/jazzy/_images/rqt_graph.png" width="560" alt="rqt_graph example">
</p>

> 노드(타원) ↔ 토픽(사각형) 관계가 한눈에 보입니다.

---

## 4. rclpy 로 내 첫 Python 노드 만들기

`rclpy` 는 ROS 2 의 Python 바인딩입니다. 토픽 하나에 메시지 보내는 publisher 와 받는 subscriber 를 만들어 봅시다.

### 4.1 패키지 스캐폴드

컨테이너 안에서:

```bash
cd /root/ros2_ws/src
ros2 pkg create --build-type ament_python my_py_pkg --dependencies rclpy std_msgs
```

### 4.2 Publisher 만들기

`examples/ros2_pubsub/minimal_publisher.py` 를 참고하세요. 핵심 코드:

```python
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
    rclpy.spin(MinimalPublisher())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

### 4.3 Subscriber 만들기

`examples/ros2_pubsub/minimal_subscriber.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__("minimal_subscriber")
        self.subscription = self.create_subscription(
            String, "chatter", self.listener_callback, 10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f"받음: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(MinimalSubscriber())
    rclpy.shutdown()
```

### 4.4 빌드 & 실행

```bash
cd /root/ros2_ws
colcon build --packages-select my_py_pkg
source install/setup.bash

# 터미널 1
ros2 run my_py_pkg publisher

# 터미널 2 (docker exec 로 새 셸)
ros2 run my_py_pkg subscriber
```

터미널 1 은 메시지를 계속 쏟아내고, 터미널 2 는 그걸 받아 출력합니다. **이게 ROS 2 통신의 전부** 입니다.

---

## 5. Track B — PyBullet 로 GPU 없이 로봇 팔 굴리기

<p align="center">
  <img src="https://pybullet.org/wordpress/wp-content/uploads/2019/03/cropped-pybullet.png" width="300" alt="PyBullet logo">
</p>

**PyBullet** 은 Bullet Physics 의 Python 바인딩. Isaac Sim 이 GPU PhysX 로 하는 일을 **CPU 로, 단순하게** 보여주는 가장 쉬운 도구입니다.

- ✅ `pip install pybullet` 한 줄
- ✅ GPU 불필요 (OpenGL 기본 렌더는 Intel Iris Plus 640 로도 됨)
- ✅ Franka Panda, Kuka IIWA 등 URDF 내장
- ✅ Headless(DIRECT) 모드로 서버/Docker 에서도 동작

### 5.1 설치 (Mac 네이티브, 가상환경)

```bash
source ~/venvs/robotics/bin/activate
pip install pybullet numpy
```

> 설치 시간 30초~1분. pip 바이너리 wheel 이 Intel Mac 용으로 바로 내려옵니다.

### 5.2 팬다 팔 로드 & 중력에 떨어뜨리기

`examples/pybullet_arm/hello_panda.py`:

```python
"""
PyBullet Hello World: Franka Panda 팔을 불러와 중력에 떨어뜨려 본다.
"""
import pybullet as p
import pybullet_data
import time

# 1. 시뮬레이터 시작 (GUI 창 띄우기. 헤드리스면 p.DIRECT)
client = p.connect(p.GUI)
p.setGravity(0, 0, -9.81, physicsClientId=client)

# 2. PyBullet 내장 URDF 경로 추가
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. 바닥과 로봇 로드
plane_id = p.loadURDF("plane.urdf")
panda_id = p.loadURDF("franka_panda/panda.urdf",
                     basePosition=[0, 0, 0],
                     useFixedBase=True)

# 4. 시뮬레이션 240Hz 로 5초
for step in range(240 * 5):
    p.stepSimulation()
    time.sleep(1.0 / 240.0)

p.disconnect()
```

```bash
python hello_panda.py
```

<p align="center">
  <img src="https://raw.githubusercontent.com/bulletphysics/bullet3/master/examples/pybullet/gym/pybullet_envs/bullet/panda_arm.png" width="420" alt="PyBullet Panda arm">
</p>

창이 뜨고 팔이 고정된 채 중력장 안에서 시뮬레이션 됩니다. 마우스로 드래그 회전, 휠 줌이 됩니다.

### 5.3 각 관절 제어

```python
# 관절 0~6 을 목표 각도로 이동 (라디안)
num_joints = p.getNumJoints(panda_id)  # 9 (joint 7개 + gripper 2개)
target_angles = [0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.7]

for i, angle in enumerate(target_angles):
    p.setJointMotorControl2(
        bodyUniqueId=panda_id,
        jointIndex=i,
        controlMode=p.POSITION_CONTROL,
        targetPosition=angle,
        force=87,
    )
```

### 5.4 헤드리스 모드 (Docker 안에서 돌릴 때)

```python
client = p.connect(p.DIRECT)  # GUI 없이, 계산만
```

`p.getCameraImage(width, height, ...)` 로 오프스크린 렌더 이미지를 numpy 로 받아올 수 있어, **강화학습 학습 루프** 에 바로 쓸 수 있습니다.

---

## 6. ROS 2 ↔ PyBullet 브리지 — "작은 Isaac Sim" 만들기

Isaac Sim 의 핵심 가치는 **"로봇 상태를 PhysX 가 돌리고, ROS 토픽으로 내보낸다"** 입니다. 이 구조를 **Docker ROS 2 + 호스트 PyBullet** 조합으로 흉내낼 수 있습니다.

### 6.1 아키텍처

```
┌──────────────────────────────┐           ┌──────────────────────────────┐
│   Docker (Linux, x86_64)     │           │   Mac host (venv, PyBullet)  │
│   ROS 2 Jazzy                │           │                              │
│                              │  DDS over │  • 시뮬레이션 루프            │
│   subscriber /joint_cmd      │◀──────────│  • JointState publisher       │
│   publisher  /joint_states   │──────────▶│  • PyBullet stepSimulation()  │
└──────────────────────────────┘ localhost └──────────────────────────────┘
```

**포인트**: ROS 2 는 DDS(Data Distribution Service)를 씁니다. Mac 에 native rclpy 를 설치하면 Docker 안 ROS 와 로컬호스트에서 서로 본인 노드를 발견합니다.

### 6.2 Mac 네이티브 `rclpy` 빠르게 쓰기

정식 방법은 시간이 오래 걸리므로, 우리는 **Python pip 로 배포되는 rclpy** 를 활용합니다:

```bash
source ~/venvs/robotics/bin/activate
pip install catkin_pkg empy==3.3.4 lark numpy  # 의존성
pip install --extra-index-url https://rospypi.github.io/simple/ rclpy sensor_msgs std_msgs
```

> ⚠️ `rospypi` 는 커뮤니티 저장소 (**비공식**). 프로덕션에서는 Docker 쪽에서 브리지 코드를 돌리거나, Mac 전체를 Ubuntu VM 에서 운용하는 게 안전합니다.

### 6.3 예제 코드

전체 파일은 [`examples/ros2_pybullet_bridge/sim_bridge.py`](examples/ros2_pybullet_bridge/sim_bridge.py) 를 보세요. 골격:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import pybullet as p
import pybullet_data


class PandaSimBridge(Node):
    def __init__(self):
        super().__init__("panda_sim_bridge")
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        self.robot = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)
        self.n = 7  # arm joints

        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        self.create_subscription(JointState, "/joint_cmd", self.cmd_cb, 10)
        self.create_timer(1 / 240.0, self.step)

    def cmd_cb(self, msg):
        for i, pos in enumerate(msg.position[: self.n]):
            p.setJointMotorControl2(self.robot, i, p.POSITION_CONTROL, pos)

    def step(self):
        p.stepSimulation()
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [f"panda_joint{i+1}" for i in range(self.n)]
        js.position = [p.getJointState(self.robot, i)[0] for i in range(self.n)]
        self.pub.publish(js)


def main():
    rclpy.init()
    rclpy.spin(PandaSimBridge())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

### 6.4 같이 실행

```bash
# 터미널 1 (Mac native venv)
source ~/venvs/robotics/bin/activate
python examples/ros2_pybullet_bridge/sim_bridge.py

# 터미널 2 (Docker ROS 2 container)
docker exec -it ros2 bash
source /opt/ros/jazzy/setup.bash
ros2 topic list        # /joint_states, /joint_cmd 가 보여야 함
ros2 topic echo /joint_states --once
```

PyBullet 창과 ROS 2 토픽이 연결된 걸 확인하면, **이 튜토리얼의 목표가 달성된 것** 입니다. 이 "작은 Isaac Sim" 의 구조를 이해하면, 진짜 Isaac Sim 의 코드도 그대로 이해됩니다.

---

## 7. Track C — 클라우드로 진짜 Isaac Sim 써 보기 (NVIDIA Brev)

NVIDIA **Brev Launchable** 은 "GPU 인스턴스 + 미리 설치된 Isaac Sim + 브라우저 기반 VS Code + Kit App 스트리밍" 를 버튼 하나로 띄워 줍니다.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/320px-Nvidia_logo.svg.png" width="180" alt="NVIDIA logo">
</p>

### 7.1 준비물

- NVIDIA 개발자 계정 (무료)
- 신용카드 (Brev 인스턴스는 유료, 시간 단위 과금 · 보통 A10/L40S 인스턴스 $0.8~$3/h)
- 최신 크롬/파이어폭스 브라우저

### 7.2 한 번에 띄우는 방법

1. [isaac-sim/isaac-launchable 리포](https://github.com/isaac-sim/isaac-launchable) 에서 **"Deploy Launchable"** 버튼 클릭.
2. Brev 로그인 → GPU 타입/지역 선택 → 시작.
3. 5~10분 기다리면 대시보드에 두 개 탭이 뜹니다:
   - VS Code (통상적인 개발 환경)
   - Kit App Streaming (Isaac Sim UI 가 브라우저로)

### 7.3 내 Intel Mac 에서는 어떻게 접속?

- ✅ 그냥 **브라우저** 로 Brev 대시보드 열기 → VS Code·Isaac Sim 둘 다 브라우저 탭 안에서 돌아감 → **Intel Mac + Ventura 에서 완전 작동**.
- ⚠️ 네이티브 "Isaac Sim WebRTC Streaming Client" macOS 앱은 존재하나 Apple Silicon 에서 렌더가 비는 이슈 ([isaac-sim/IsaacSim#103](https://github.com/isaac-sim/IsaacSim/issues/103)) 가 보고됨. Intel Mac 에선 더 안정적이라는 리포트도 있으나 보장 안 됨.

### 7.4 안 쓸 때 반드시 인스턴스 정지!

요금은 **실행 중일 때** 과금됩니다. 작업 끝나면 Brev 대시보드에서 **Stop** 버튼 필수.

---

## 8. 다음 단계 — 추천 학습 로드맵

```
[입문]   ROS 2 Docker + turtlesim      (이 튜토리얼)
   ↓
[기초]   rclpy pub/sub + 사용자 메시지
   ↓
[실습]   PyBullet Panda + RL (gymnasium + stable-baselines3)
   ↓
[중급]   Gazebo Harmonic + ros_gz (Docker)
   ↓
[고급]   NVIDIA Brev Isaac Sim / Isaac Lab
   ↓
[전문]   Isaac Lab 에서 RL, Cosmos World Model 연동
```

추천 다음 자료:
- **[ROS 2 Jazzy 공식 튜토리얼](https://docs.ros.org/en/jazzy/Tutorials.html)** — Beginner → Intermediate 순차 진행
- **[Isaac Sim 5.x 공식 도큐](https://docs.isaacsim.omniverse.nvidia.com/)**
- **[Isaac Lab 튜토리얼](https://isaac-sim.github.io/IsaacLab/)** — RL 중심
- **[Gazebo Harmonic 튜토리얼](https://gazebosim.org/docs/harmonic/tutorials)** — 오픈소스 시뮬
- **[PybulletRobotics 예제 모음](https://github.com/akinami3/PybulletRobotics)** — Python 레벨 로봇 예제 다수

---

## 9. 트러블슈팅 FAQ

### 9.1 "Cannot connect to the Docker daemon"
→ Docker Desktop 앱이 실행 중인지 확인. 메뉴 막대 🐳 아이콘이 "running" 상태여야 함.

### 9.2 GUI 창이 안 떠요 (XQuartz)
1. XQuartz **설정에서 "Allow connections from network clients" 체크 후 완전 재시작** 했는지
2. 터미널에서 `xhost + 127.0.0.1` 를 매 세션마다 실행했는지
3. Docker 명령에 `-e DISPLAY=host.docker.internal:0` 가 정확히 들어갔는지
4. `echo $DISPLAY` 가 컨테이너 안에서 `host.docker.internal:0` 로 나오는지

### 9.3 `ros2 run` 이 "command not found"
→ `source /opt/ros/jazzy/setup.bash` 를 새 셸마다 실행해야 합니다. `.bashrc` 에 넣으세요.

### 9.4 PyBullet 창이 검게 뜹니다
Intel Iris Plus Graphics 에서 드물게 발생. 해결:
```python
p.connect(p.GUI, options="--opengl2")   # 구 OpenGL 강제
# 또는 헤드리스로:
p.connect(p.DIRECT)
```

### 9.5 Docker 이미지가 너무 커요
`jazzy-ros-base` 로 바꾸면 약 700MB (단, turtlesim/RViz 없음). 학습용으론 `jazzy-desktop` 을 권장.

### 9.6 macOS 13.7 Ventura 에서 brew 패키지가 "unsupported"
최신 Homebrew 는 Sonoma/Sequoia/Tahoe 쪽에 초점이 있어 Ventura 에서 bottle 을 못 찾고 소스 빌드를 시도할 수 있습니다. 대부분 괜찮지만, 실패하면 `brew install --build-from-source <pkg>` 를 시도하거나 Docker 쪽으로 해당 작업을 옮기세요.

### 9.7 Brev 가 "no capacity" 라고 나와요
데이터센터 지역(us-east-1 등) 을 바꾸거나, 낮은 등급(L4, A10) 으로 시도.

---

## 10. 참고 자료

### ROS 2
- [ROS 2 Jazzy 공식 설치 (macOS source)](https://docs.ros.org/en/jazzy/Installation/Alternatives/macOS-Development-Setup.html)
- [Docker 공식 ROS 2 Turtlesim 가이드](https://docs.docker.com/guides/ros2/turtlesim-example/)
- [Foxglove — Installing ROS 2 on macOS with Docker](https://foxglove.dev/blog/installing-ros2-on-macos-with-docker)
- [Automatic Addison — Publisher/Subscriber (Jazzy)](https://automaticaddison.com/how-to-create-a-ros-2-python-publisher-jazzy/)
- [Docker Hub — osrf/ros 태그](https://hub.docker.com/r/osrf/ros/tags)

### Isaac Sim / Isaac Lab
- [Isaac Sim 공식 다운로드](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html)
- [Isaac Sim WebRTC Streaming Clients](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html)
- [NVIDIA Brev Launchable 리포 (isaac-sim/isaac-launchable)](https://github.com/isaac-sim/isaac-launchable)
- [Isaac Lab Docker Guide](https://isaac-sim.github.io/IsaacLab/main/source/deployment/docker.html)
- [Isaac Sim Cloud Deployment](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_cloud.html)
- [Isaac Sim WebRTC Mac 이슈 트래커 (#103)](https://github.com/isaac-sim/IsaacSim/issues/103)

### 물리 시뮬레이터
- [PyBullet 공식](https://pybullet.org/)
- [PyBullet PyPI](https://pypi.org/project/pybullet/)
- [PybulletRobotics 예제 모음](https://github.com/akinami3/PybulletRobotics)
- [MuJoCo 공식 (Python)](https://mujoco.readthedocs.io/)

### Apple Silicon 사용자를 위한 보너스 링크 (참고만)
- [IOES-Lab ROS2_Jazzy_MacOS_Native_AppleSilicon](https://github.com/IOES-Lab/ROS2_Jazzy_MacOS_Native_AppleSilicon) — **Apple Silicon only**
- [idesign0/gz-macOS](https://github.com/idesign0/gz-macOS) — Apple Silicon Gazebo

### X11 / GUI
- [XQuartz 공식](https://www.xquartz.org/)
- [X11 forwarding with macOS and Docker (Gist)](https://gist.github.com/sorny/969fe55d85c9b0035b0109a31cbcb088)

---

> 💡 이 튜토리얼은 **공식 자료가 아닌 개인 학습 요약** 입니다. 오류 지적이나 개선 제안은 이슈/PR 로 환영합니다.
