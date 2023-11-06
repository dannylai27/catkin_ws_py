// -->subsrcibe to 'vel_array'
// publish '


// required library
// ROS
#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY

#include <ros.h>
#include <std_msgs/Float64.h>

// Stepper
#include <TMC2130Stepper.h>
#include <AccelStepper.h>



// TMC2130 & encoder set-up
// defines pins numbers
// motor 4/M4
// motor 3/M3
#define EN_PIN_M3    14  //enable (CFG6)
#define DIR_PIN_M3   16  //direction
#define STEP_PIN_M3  15  //step
#define CS_PIN_M3    17  //chip select
// motor 4/M4
#define EN_PIN_M4    18  //enable (CFG6)
#define DIR_PIN_M4   20  //direction
#define STEP_PIN_M4  19  //step
#define CS_PIN_M4    21  //chip select

// initialize TMC2130 driver & encoder
int microstepping = 2;
// M3
TMC2130Stepper TMC2130_M3 = TMC2130Stepper(EN_PIN_M3, DIR_PIN_M3, STEP_PIN_M3, CS_PIN_M3);
AccelStepper stepper_M3(1, STEP_PIN_M3, DIR_PIN_M3); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// M4
TMC2130Stepper TMC2130_M4 = TMC2130Stepper(EN_PIN_M4, DIR_PIN_M4, STEP_PIN_M4, CS_PIN_M4);
AccelStepper stepper_M4(1, STEP_PIN_M4, DIR_PIN_M4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


//must declaration
// ROS
ros::NodeHandle nh;

float vel_stepper_M3_desired=0.0, vel_stepper_M4_desired=0.0;
//double a = 0.0;

// msgs needed


//callback function
void vel_array_Cb_M3(const std_msgs::Float64 &msg){
  
  vel_stepper_M3_desired = int(msg.data);
  stepper_M3.setSpeed(vel_stepper_M3_desired);
}

void vel_array_Cb_M4(const std_msgs::Float64 &msg){
  
  vel_stepper_M4_desired = int(msg.data);
  stepper_M4.setSpeed(vel_stepper_M4_desired);
}
// subscriber for arduino
ros::Subscriber<std_msgs::Float64> s_M3("vel_array_M3", &vel_array_Cb_M3);
ros::Subscriber<std_msgs::Float64> s_M4("vel_array_M4", &vel_array_Cb_M4);


// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;

void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.subscribe(s_M3);
  nh.subscribe(s_M4);

  delay(1000);

  // TMC2130 setup
  // Sets the two pins as Outputs
  //M3:
  pinMode(EN_PIN_M3,OUTPUT); 
  pinMode(DIR_PIN_M3,OUTPUT);
  digitalWrite(DIR_PIN_M3,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(EN_PIN_M3,LOW);
  TMC2130_M3.begin(); // Initiate pins and registeries
  TMC2130_M3.SilentStepStick2130(1300); // Set stepper current to 600mA
  TMC2130_M3.stealthChop(1); // Enable extremely quiet stepping
  TMC2130_M3.microsteps(microstepping);
  digitalWrite(EN_PIN_M3, LOW);
  stepper_M3.setMaxSpeed(2000);
  stepper_M3.setSpeed(0.0);

  //M4:
  pinMode(EN_PIN_M4,OUTPUT); 
  pinMode(DIR_PIN_M4,OUTPUT);
  digitalWrite(DIR_PIN_M4,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(EN_PIN_M4,LOW);
  TMC2130_M4.begin(); // Initiate pins and registeries
  TMC2130_M4.SilentStepStick2130(1300); // Set stepper current to 600mA
  TMC2130_M4.stealthChop(1); // Enable extremely quiet stepping
  TMC2130_M4.microsteps(microstepping);
  digitalWrite(EN_PIN_M4, LOW);
  stepper_M4.setMaxSpeed(2000); //?? is 500 the max?
  stepper_M4.setSpeed(0.0);

  
}

void loop()
{
  stepper_M3.runSpeed();
  stepper_M4.runSpeed();


  now = millis();

  if ((now - lasttimepub)> 16) // !!!10 will very likely to fail.
    {

      lasttimepub=now;
    }

  nh.spinOnce();
}
