#include <ros_control_example/robot_hardware_interface.h>

ROBOTHardwareInterface::ROBOTHardwareInterface(ros::NodeHandle& nh) : nh_(nh) {
    init();
    controller_manager_.reset(new controller_manager::ControllerManager(this, nh_));
    loop_hz_=40; 
    ros::Duration update_freq = ros::Duration(1.0/loop_hz_);
	
	pub_1 = nh_.advertise<rospy_tutorials::Floats>("/joints_to_aurdino_1",2);
	client_1 = nh_.serviceClient<ros_control_example::Floats_array>("/read_joint_state_1");
	
	pub_2 = nh_.advertise<rospy_tutorials::Floats>("/joints_to_aurdino_2",2);
	client_2 = nh_.serviceClient<ros_control_example::Floats_array>("/read_joint_state_2");
	

	
    non_realtime_loop_ = nh_.createTimer(update_freq, &ROBOTHardwareInterface::update, this);
}

ROBOTHardwareInterface::~ROBOTHardwareInterface() {
}

void ROBOTHardwareInterface::init() {
    
    
	joint_name_[0]="joint1";
    
// Create joint state interface
    hardware_interface::JointStateHandle jointStateHandle_1(joint_name_[0], &joint_position_[0], &joint_velocity_[0], &joint_effort_[0]);
    joint_state_interface_.registerHandle(jointStateHandle_1);


// Create effort joint interface
    hardware_interface::JointHandle jointEffortHandle_1(jointStateHandle_1, &joint_effort_command_[0]);
	effort_joint_interface_.registerHandle(jointEffortHandle_1);
	
// Create Joint Limit interface   
    joint_limits_interface::JointLimits limits;
    joint_limits_interface::getJointLimits(joint_name_[0], nh_, limits);
	joint_limits_interface::EffortJointSaturationHandle jointLimitsHandle_1(jointEffortHandle_1, limits);
	effortJointSaturationInterface.registerHandle(jointLimitsHandle_1);
	
/*
If you have more joints then,
*/
    joint_name_[1]= "joint2";
    
// Create joint state interface
    hardware_interface::JointStateHandle jointStateHandle_2(joint_name_[1], &joint_position_[1], &joint_velocity_[1], &joint_effort_[1]);
    joint_state_interface_.registerHandle(jointStateHandle_2);

//create the position/velocity/effort interface according to your actuator 
  
    hardware_interface::JointHandle jointEffortHandle_2(jointStateHandle_2, &joint_effort_command_[1]);
	effort_joint_interface_.registerHandle(jointEffortHandle_2);
	
//create joint limit interface.
    joint_limits_interface::getJointLimits(joint_name_[1], nh_, limits);
	joint_limits_interface::EffortJointSaturationHandle jointLimitsHandle_2(jointEffortHandle_2, limits);
	effortJointSaturationInterface.registerHandle(jointLimitsHandle_2);
	
/*	Repeat same for other joints
*/
	

// Register all joints interfaces    
    registerInterface(&joint_state_interface_);
    registerInterface(&position_joint_interface_);
    registerInterface(&effort_joint_interface_);
    registerInterface(&effortJointSaturationInterface);
}
// da qui in giù va sistemato



void ROBOTHardwareInterface::update(const ros::TimerEvent& e) {
    elapsed_time_ = ros::Duration(e.current_real - e.last_real);
    read();
    controller_manager_->update(ros::Time::now(), elapsed_time_);
    write(elapsed_time_);
}

void ROBOTHardwareInterface::read() {

	joint_read_1.request.req=1.0;
	
	if(client_1.call(joint_read_1))
	{
	    joint_position_[0] = angles::from_degrees(joint_read_1.response.res[0]);
	    joint_velocity_[0] = angles::from_degrees(joint_read_1.response.res[1]);
	    ROS_INFO("Current Pos_1: %.2f, Vel_1: %.2f",joint_position_[0],joint_velocity_[0]);

	}
	else
	{
	    joint_position_[0] = 0;
	    joint_velocity_[0] = 0;
	}
	
	joint_read_2.request.req=1.0;
	
	if(client_2.call(joint_read_2))
	{
	    joint_position_[1] = angles::from_degrees(joint_read_2.response.res[0]);
	    joint_velocity_[1] = angles::from_degrees(joint_read_2.response.res[1]);
	    ROS_INFO("Current Pos_2: %.2f, Vel_2: %.2f",joint_position_[1],joint_velocity_[1]);
    
	}
	else
	{
	    joint_position_[1] = 0;
	    joint_velocity_[1] = 0;
	}
        

}

void ROBOTHardwareInterface::write(ros::Duration elapsed_time) {
   
    effortJointSaturationInterface.enforceLimits(elapsed_time);    
	joints_pub_1.data.clear();
	joints_pub_1.data.push_back(joint_effort_command_[0]);
	
	ROS_INFO("PWM_1 Cmd: %.2f",joint_effort_command_[0]);
	pub_1.publish(joints_pub_1);


	joints_pub_2.data.clear();
	joints_pub_2.data.push_back(joint_effort_command_[1]);
		
	ROS_INFO("PWM_2 Cmd: %.2f",joint_effort_command_[1]);
	pub_2.publish(joints_pub_2);
		
}



int main(int argc, char** argv)
{
    ros::init(argc, argv, "single_joint_hardware_interface");
    ros::NodeHandle nh;
    //ros::AsyncSpinner spinner(4);  
    ros::MultiThreadedSpinner spinner(2); // Multiple threads for controller service callback and for the Service client callback used to get the feedback from ardiuno
    ROBOTHardwareInterface ROBOT(nh);
    //spinner.start();
    spinner.spin();
    //ros::spin();
    return 0;
}








/*




void ROBOTHardwareInterface::update(const ros::TimerEvent& e) {
    elapsed_time_ = ros::Duration(e.current_real - e.last_real);
    read();
    controller_manager_->update(ros::Time::now(), elapsed_time_);
    write(elapsed_time_);
}

void ROBOTHardwareInterface::read() {

	joint_read.request.req=1.0;
	
	if(client.call(joint_read))
	{
	    joint_position_ = angles::from_degrees(joint_read.response.res[0]);
	    joint_velocity_ = angles::from_degrees(joint_read.response.res[1]);
	    ROS_INFO("Current Pos: %.2f, Vel: %.2f",joint_position_,joint_velocity_);

if more than one joint,
        get values for joint_position_2, joint_velocity_2,......
	    
	    
	}
	else
	{
	    joint_position_ = 0;
	    joint_velocity_ = 0;
	}
        

}

void ROBOTHardwareInterface::write(ros::Duration elapsed_time) {
   
    effortJointSaturationInterface.enforceLimits(elapsed_time);    
	joints_pub.data.clear();
	joints_pub.data.push_back(joint_effort_command_);
	

if more than one joint,
    publish values for joint_effort_command_2,......
	
	
	ROS_INFO("PWM Cmd: %.2f",joint_effort_command_);
	pub.publish(joints_pub);
		
}



int main(int argc, char** argv)
{
    ros::init(argc, argv, "single_joint_hardware_interface");
    ros::NodeHandle nh;
    //ros::AsyncSpinner spinner(4);  
    ros::MultiThreadedSpinner spinner(2); // Multiple threads for controller service callback and for the Service client callback used to get the feedback from ardiuno
    ROBOTHardwareInterface ROBOT(nh);
    //spinner.start();
    spinner.spin();
    //ros::spin();
    return 0;
}


*/







