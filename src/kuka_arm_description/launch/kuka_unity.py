from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            get_package_share_directory("kuka_arm_description"),
            "urdf",
            "robot_arm_description.SLDASM.urdf.xacro"
        ),
        description="Absolute path to the robot URDF file"
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(
            get_package_share_directory("kuka_arm_description"),
            "rviz",
            "display.rviz"
        )]
    )

    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            os.path.join(
                get_package_share_directory("kuka_arm_controller"),
                "config",
                "kuka_arm_controller.yaml"
            )
        ],
        output="screen"
    )

    controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["kuka_arm_controller"],
        output="screen"
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node,
        controller_manager_node,
        controller_spawner
    ])
