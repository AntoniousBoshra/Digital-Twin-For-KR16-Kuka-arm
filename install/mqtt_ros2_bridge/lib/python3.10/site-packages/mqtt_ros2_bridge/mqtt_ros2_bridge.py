import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import paho.mqtt.client as mqtt
import json

class MqttRos2Bridge(Node):
    def __init__(self):
        super().__init__('mqtt_ros2_bridge')
        self.publisher = self.create_publisher(JointTrajectory, '/position_trajectory_controller/joint_trajectory', 10)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("broker.hivemq.com", 1883, 60)  # Replace with your broker IP
        self.mqtt_client.subscribe("robot/joint_positions")  # Topic to subscribe to

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"Connected to MQTT Broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            joint_trajectory = JointTrajectory()
            joint_trajectory.header.stamp.sec = 0
            joint_trajectory.header.stamp.nanosec = 0

            # Set default joint names (you can adjust these as needed)
            joint_trajectory.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

            # Create a JointTrajectoryPoint and assign the received positions
            point = JointTrajectoryPoint()
            point.positions = data
            point.time_from_start.sec = 2  # Set a default time for the trajectory
            point.time_from_start.nanosec = 0
            joint_trajectory.points.append(point)

            # Publish the joint trajectory message
            self.publisher.publish(joint_trajectory)
        except Exception as e:
            self.get_logger().error(f"Failed to process MQTT message: {e}")

    def run(self):
        while rclpy.ok():
            self.mqtt_client.loop()
            rclpy.spin_once(self)

def main(args=None):
    rclpy.init(args=args)
    mqtt_ros2_bridge = MqttRos2Bridge()
    mqtt_ros2_bridge.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
