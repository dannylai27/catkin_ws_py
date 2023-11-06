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
// motor 4/M2
// motor 3/M1
#define EN_PIN_M1    13  //enable (CFG6)
#define DIR_PIN_M1   11  //direction
#define STEP_PIN_M1  12  //step
#define CS_PIN_M1    10  //chip select
// motor 4/M2
#define EN_PIN_M2    9  //enable (CFG6)
#define DIR_PIN_M2   7  //direction
#define STEP_PIN_M2  8  //step
#define CS_PIN_M2    6  //chip select

// initialize TMC2130 driver & encoder
int microstepping = 2;
// M1
TMC2130Stepper TMC2130_M1 = TMC2130Stepper(EN_PIN_M1, DIR_PIN_M1, STEP_PIN_M1, CS_PIN_M1);
AccelStepper stepper_M1(1, STEP_PIN_M1, DIR_PIN_M1); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// M2
TMC2130Stepper TMC2130_M2 = TMC2130Stepper(EN_PIN_M2, DIR_PIN_M2, STEP_PIN_M2, CS_PIN_M2);
AccelStepper stepper_M2(1, STEP_PIN_M2, DIR_PIN_M2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


//must declaration
// ROS
ros::NodeHandle nh;

float vel_stepper_M1_desired=0.0, vel_stepper_M2_desired=0.0;
//double a = 0.0;

// msgs needed


//callback function
void vel_array_Cb_M1(const std_msgs::Float64 &msg){
  
  vel_stepper_M1_desired = int(msg.data);
  stepper_M1.setSpeed(vel_stepper_M1_desired);
}

void vel_array_Cb_M2(const std_msgs::Float64 &msg){
  
  vel_stepper_M2_desired = int(msg.data);
  stepper_M2.setSpeed(vel_stepper_M2_desired);
}
// subscriber for arduino
ros::Subscriber<std_msgs::Float64> s_M1("vel_array_M1", &vel_array_Cb_M1);
ros::Subscriber<std_msgs::Float64> s_M2("vel_array_M2", &vel_array_Cb_M2);


// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;

void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.subscribe(s_M1);
  nh.subscribe(s_M2);

  delay(1000);

  // TMC2130 setup
  // Sets the two pins as Outputs
  //M1:
  pinMode(EN_PIN_M1,OUTPUT); 
  pinMode(DIR_PIN_M1,OUTPUT);
  digitalWrite(DIR_PIN_M1,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(EN_PIN_M1,LOW);
  TMC2130_M1.begin(); // Initiate pins and registeries
  TMC2130_M1.SilentStepStick2130(1300); // Set stepper current to 600mA
  TMC2130_M1.stealthChop(1); // Enable extremely quiet stepping
  TMC2130_M1.microsteps(microstepping);
  digitalWrite(EN_PIN_M1, LOW);
  stepper_M1.setMaxSpeed(2000);
  stepper_M1.setSpeed(0.0);

  //M2:
  pinMode(EN_PIN_M2,OUTPUT); 
  pinMode(DIR_PIN_M2,OUTPUT);
  digitalWrite(DIR_PIN_M2,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(EN_PIN_M2,LOW);
  TMC2130_M2.begin(); // Initiate pins and registeries
  TMC2130_M2.SilentStepStick2130(1300); // Set stepper current to 600mA
  TMC2130_M2.stealthChop(1); // Enable extremely quiet stepping
  TMC2130_M2.microsteps(microstepping);
  digitalWrite(EN_PIN_M2, LOW);
  stepper_M2.setMaxSpeed(2000); //?? is 500 the max?
  stepper_M2.setSpeed(0.0);

  
}

void loop()
{
  stepper_M1.runSpeed();
  stepper_M2.runSpeed();


  now = millis();

  if ((now - lasttimepub)> 16) // !!!10 will very likely to fail.
    {

      lasttimepub=now;
    }

  nh.spinOnce();
}
