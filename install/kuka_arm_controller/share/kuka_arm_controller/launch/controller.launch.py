from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Get the robot description (URDF generated from xacro)
    robot_description_content = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("kuka_arm_description"),
            "urdf",
            "robot_arm_description.SLDASM.urdf.xacro"
        ])
    ])

    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    # Load controller configuration YAML
    controller_config = PathJoinSubstitution([
        FindPackageShare("kuka_arm_controller"),
        "config",
        "kuka_arm_controller.yaml"
    ])

    # robot_state_publisher node
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="screen"
    )

    # ros2_control node
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config],
        output="screen"
    )

    # Spawner for joint_state_broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        parameters=[{"use_sim_time": False}],
        output="screen"
    )

    # Spawner for robot controller
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["position_trajectory_controller", "--controller-manager", "/controller_manager"],
        parameters=[{"use_sim_time": False}],
        output="screen"
    )

    return LaunchDescription([
        robot_state_publisher_node,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        robot_controller_spawner
    ])
