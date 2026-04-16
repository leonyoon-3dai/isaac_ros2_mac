"""ROS 2 ament_python 패키지 `my_py_pkg` 의 setup.py 예시.

빌드된 패키지 배치:
    ros2_ws/
      src/
        my_py_pkg/
          setup.py            (이 파일)
          package.xml
          my_py_pkg/
            __init__.py
            minimal_publisher.py
            minimal_subscriber.py
"""

from setuptools import setup

package_name = "my_py_pkg"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="leonyoon",
    maintainer_email="leonyoon@gmail.com",
    description="Intel Mac 에서 Docker ROS 2 Jazzy 로 돌리는 pub/sub 최소 예제",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "publisher  = my_py_pkg.minimal_publisher:main",
            "subscriber = my_py_pkg.minimal_subscriber:main",
        ],
    },
)
