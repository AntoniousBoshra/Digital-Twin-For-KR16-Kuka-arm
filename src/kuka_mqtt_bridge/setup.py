from setuptools import setup

package_name = 'kuka_mqtt_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools', 'paho-mqtt'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your@email.com',
    description='MQTT to JointTrajectory bridge for KUKA arm',
    license='MIT',
    entry_points={
        'console_scripts': [
            'mqtt_to_trajectory = kuka_mqtt_bridge.mqtt_to_trajectory:main',
        ],
    },
)
