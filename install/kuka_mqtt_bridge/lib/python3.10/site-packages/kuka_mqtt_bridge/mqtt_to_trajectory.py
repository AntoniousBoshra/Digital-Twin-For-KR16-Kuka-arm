import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import paho.mqtt.client as mqtt
import json

class MQTTJointBridge(Node):
    def __init__(self):
        super().__init__('mqtt_joint_bridge')

        self.publisher_ = self.create_publisher(JointTrajectory, '/position_trajectory_controller/joint_trajectory', 10)

        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect('broker.emqx.io', 1883, 60)  # Update with your broker IP
        self.mqtt_client.loop_start()

        self.mqtt_client.subscribe("kuka/joint_positions")
        self.get_logger().info("Subscribed to MQTT topic: kuka/joint_positions")

    def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"Connected to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            positions = payload.get("positions", [])
            if len(positions) == 6:
                traj_msg = JointTrajectory()
                traj_msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

                point = JointTrajectoryPoint()
                point.positions = positions
                point.time_from_start.sec = 2

                traj_msg.points.append(point)

                self.publisher_.publish(traj_msg)
                self.get_logger().info(f"Published joint positions: {positions}")
            else:
                self.get_logger().warn("Invalid joint count received")
        except Exception as e:
            self.get_logger().error(f"Error parsing MQTT message: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = MQTTJointBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
