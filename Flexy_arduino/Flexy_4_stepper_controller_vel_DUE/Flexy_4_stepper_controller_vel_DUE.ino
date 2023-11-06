
// required library
// ROS
#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY
#include <ros.h>
#include <rospy_tutorials/Floats.h>

// Stepper
#include <TMC2130Stepper.h>
#include <AccelStepper.h>



// TMC2130 & encoder set-up
// defines pins numbers
// motor 1/M1
#define EN_PIN_M1    13  //enable (CFG6)
#define DIR_PIN_M1   11  //direction
#define STEP_PIN_M1  12  //step
#define CS_PIN_M1    10  //chip select
// motor 2/M2
#define EN_PIN_M2    9  // Nano v3:  16 Mega:  38  UNO:  7 //enable (CFG6)
#define DIR_PIN_M2   7  //           19        55        8 //direction
#define STEP_PIN_M2  8  //           18        54        9 //step
#define CS_PIN_M2    6  //           17        64        10//chip select
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
int microstepping = 4;
// M1
TMC2130Stepper TMC2130_M1 = TMC2130Stepper(EN_PIN_M1, DIR_PIN_M1, STEP_PIN_M1, CS_PIN_M1);
AccelStepper stepper_M1(1, STEP_PIN_M1, DIR_PIN_M1); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// M2
TMC2130Stepper TMC2130_M2 = TMC2130Stepper(EN_PIN_M2, DIR_PIN_M2, STEP_PIN_M2, CS_PIN_M2);
AccelStepper stepper_M2(1, STEP_PIN_M2, DIR_PIN_M2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// M3
TMC2130Stepper TMC2130_M3 = TMC2130Stepper(EN_PIN_M3, DIR_PIN_M3, STEP_PIN_M3, CS_PIN_M3);
AccelStepper stepper_M3(1, STEP_PIN_M3, DIR_PIN_M3); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// M4
TMC2130Stepper TMC2130_M4 = TMC2130Stepper(EN_PIN_M4, DIR_PIN_M4, STEP_PIN_M4, CS_PIN_M4);
AccelStepper stepper_M4(1, STEP_PIN_M4, DIR_PIN_M4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


//must declaration
// ROS
ros::NodeHandle nh;

float vel_x=0.0, vel_y =0.0, vel_stepper_M1=0.0, vel_stepper_M2=0.0, vel_stepper_M3=0.0, vel_stepper_M4=0.0;
float vel_stepper_M1_desired=0.0, vel_stepper_M2_desired=0.0, vel_stepper_M3_desired=0.0, vel_stepper_M4_desired=0.0;
float joy_left_LR = 0.1, joy_left_UD = 0.0, joy_right_LR = 0.0, joy_right_UD = 0.0;
int button_X = 0, button_O = 0, button_Tri = 0, button_Squ = 0;
double a = 0.0;

// msgs needed
rospy_tutorials::Floats joy_states;



//callback function
void messageCb( const rospy_tutorials::Floats &msg){
  joy_states = msg;
  vel_stepper_M1_desired = int(joy_states.data[0]);
  vel_stepper_M2_desired = int(joy_states.data[1]);
  vel_stepper_M3_desired = int(joy_states.data[2]);
  vel_stepper_M4_desired = int(joy_states.data[3]);
  stepper_M1.setSpeed(vel_stepper_M1_desired);
  stepper_M2.setSpeed(vel_stepper_M2_desired);
  stepper_M3.setSpeed(vel_stepper_M3_desired);
  stepper_M4.setSpeed(vel_stepper_M4_desired);

}
// subscriber for arduino
ros::Subscriber<rospy_tutorials::Floats> s("vel_array", &messageCb);



// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.subscribe(s);
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
  stepper_M1.setMaxSpeed(10000);
  stepper_M1.setSpeed(0);
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
  stepper_M2.setMaxSpeed(10000);
  stepper_M2.setSpeed(0);
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
  stepper_M3.setMaxSpeed(10000);
  stepper_M3.setSpeed(0);
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
  stepper_M4.setMaxSpeed(10000);
  stepper_M4.setSpeed(0);  
}

void loop()
{
  stepper_M1.runSpeed();
  stepper_M2.runSpeed();
  stepper_M3.runSpeed();
  stepper_M4.runSpeed();
  nh.spinOnce();
}
