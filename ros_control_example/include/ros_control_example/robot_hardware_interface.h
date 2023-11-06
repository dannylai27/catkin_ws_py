#include <hardware_interface/joint_state_interface.h>
#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/robot_hw.h>
#include <joint_limits_interface/joint_limits.h>
#include <joint_limits_interface/joint_limits_interface.h>
#include <joint_limits_interface/joint_limits_rosparam.h>
#include <joint_limits_interface/joint_limits_urdf.h>
#include <controller_manager/controller_manager.h>
#include <boost/scoped_ptr.hpp>
#include <ros/ros.h>
#include <rospy_tutorials/Floats.h>
#include <ros_control_example/Floats_array.h>
#include <angles/angles.h>

class ROBOTHardwareInterface : public hardware_interface::RobotHW 
{
	public:
        ROBOTHardwareInterface(ros::NodeHandle& nh);
        ~ROBOTHardwareInterface();
        void init();
        void update(const ros::TimerEvent& e);
        void read();
        void write(ros::Duration elapsed_time);
        ros::Publisher pub_1,pub_2;
        ros::ServiceClient client_1,client_2;
        rospy_tutorials::Floats joints_pub_1,joints_pub_2;
        ros_control_example::Floats_array joint_read_1,joint_read_2;
        
    protected:
        hardware_interface::JointStateInterface joint_state_interface_;
        hardware_interface::PositionJointInterface position_joint_interface_;
        hardware_interface::EffortJointInterface     effort_joint_interface_;

        
        joint_limits_interface::EffortJointSaturationInterface effortJointSaturationInterface;
        

	//we have more than 1 joint so we use arrays, in each array the first element is related to the joint number 1 while the second element is releted to the joint number 2

        int num_joints_[2];
        std::string joint_name_[2];  
        double joint_position_[2];
        double joint_velocity_[2];
        double joint_effort_[2];
        double joint_position_command_[2];
        double joint_effort_command_[2];
        double joint_velocity_command_[2];
        
        ros::NodeHandle nh_;
        ros::Timer non_realtime_loop_;
        ros::Duration elapsed_time_;
        double loop_hz_;
        boost::shared_ptr<controller_manager::ControllerManager> controller_manager_;
};

