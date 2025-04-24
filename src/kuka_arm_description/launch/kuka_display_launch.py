# Import core ROS 2 launch classes and utilities
from launch import LaunchDescription  # Used to define and return the complete launch setup
from launch.actions import DeclareLaunchArgument  # Allows passing arguments to the launch file
from launch_ros.actions import Node  # Used to start ROS 2 nodes
from launch_ros.parameter_descriptions import ParameterValue  # Allows dynamic parameter definition
from launch.substitutions import Command, LaunchConfiguration  # Substitution: dynamic command execution and argument access
import os  # Standard Python module for file and path operations
from ament_index_python.packages import get_package_share_directory  # Finds the share directory of a given package

# Main function called when the launch file is executed
def generate_launch_description():
    # Declare a launch argument 'model' with a default value pointing to the robot's Xacro (URDF macro) file
    model_arg = DeclareLaunchArgument(
        name="model",  # Name of the argument
        default_value=os.path.join(  # Construct the default path to the Xacro file
            get_package_share_directory("kuka_arm_description"),  # Get the share directory of the 'kuka_arm_description' package
            "urdf",  # Folder containing the URDF/Xacro files
            "robot_arm_description.SLDASM.urdf.xacro"  # The specific Xacro file name
        ),
        description="Absolute path to the robot URDF file"  # Description of the argument for users
    )

    # Create a parameter for 'robot_description' by processing the Xacro file
    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),  # Run 'xacro' on the given model path
        value_type=str  # The result is expected to be a string (the URDF XML)
    )

    # Define the robot_state_publisher node, which publishes the robot's kinematic state
    robot_state_publisher = Node(
        package="robot_state_publisher",  # ROS 2 package that provides the node
        executable="robot_state_publisher",  # Name of the executable node
        parameters=[{"robot_description": robot_description}]  # Provide the robot description as a parameter
    )

    # Define the joint_state_publisher_gui node, which provides a GUI to manually adjust joint states
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",  # ROS 2 package that contains the GUI tool
        executable="joint_state_publisher_gui"  # Launch the GUI tool
    )

    # Define the RViz visualization node, which will show the robot model and its state
    rviz_node = Node(
        package="rviz2",  # Package for RViz 2
        executable="rviz2",  # The RViz 2 executable
        name="rviz2",  # Name of the node
        output="screen",  # Print output to the terminal
        arguments=["-d", os.path.join(  # Load a specific RViz configuration file
            get_package_share_directory("kuka_arm_description"),  # Path to the 'kuka_arm_description' package
            "rviz",  # Subfolder containing RViz config
            "display.rviz"  # Specific RViz config file
        )]
    )

    # Return all launch elements as a LaunchDescription object
    return LaunchDescription([
        model_arg,  # Include the declared launch argument
        robot_state_publisher,  # Include the robot state publisher node
        joint_state_publisher_gui,  # Include the joint state GUI node
        rviz_node  # Include the RViz node
    ])
