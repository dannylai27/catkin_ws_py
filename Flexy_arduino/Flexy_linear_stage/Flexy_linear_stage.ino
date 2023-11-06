
// required library
// ROS
#include <ros.h>
#include <std_msgs/Float64.h>
// Stepper
#include <TMC2130Stepper.h>
#include <AccelStepper.h>



// TMC2130 set-up
// defines pins numbers
#define EN_PIN    7  // Nano v3:  16 Mega:  38  UNO:  7 //enable (CFG6)
#define DIR_PIN   8  //           19        55        8 //direction
#define STEP_PIN  9  //           18        54        9 //step
#define CS_PIN    10 //           17        64        10//chip select

// initialize TMC2130 driver
int microstepping = 32;
int one_revolution = 200 * microstepping;
const int motorSpeedLinearStage = 50;
TMC2130Stepper TMC2130 = TMC2130Stepper(EN_PIN, DIR_PIN, STEP_PIN, CS_PIN);

// AccelStepper library set-up
AccelStepper stepper(1, 9, 8); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


//must declaration
// ROS
ros::NodeHandle nh;

float vel_x=0.0, vel_y =0.0, vel_stepper=0.0;
// msgs needed
std_msgs::Float64 motor_speed;

//callback function
void messageCb( const std_msgs::Float64 &msg){
  vel_stepper = int(msg.data);
  stepper.setSpeed(-vel_stepper);
}
// subscriber for arduino
ros::Subscriber<std_msgs::Float64> s("desired_stepper_speed", &messageCb);
// publisher for arduino
ros::Publisher p("encoder_stepper", &motor_speed);

// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.advertise(p);
  nh.subscribe(s);

    // TMC2130 setup
  // Sets the two pins as Outputs
  pinMode(EN_PIN,OUTPUT); 
  pinMode(DIR_PIN,OUTPUT);
  digitalWrite(DIR_PIN,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(EN_PIN,LOW);
  
  TMC2130.begin(); // Initiate pins and registeries
  TMC2130.SilentStepStick2130(900); // Set stepper current to 600mA
  TMC2130.stealthChop(1); // Enable extremely quiet stepping
  TMC2130.microsteps(microstepping);
  digitalWrite(EN_PIN, LOW);
  
  stepper.setMaxSpeed(10000);
  stepper.setSpeed(0);  
//  stepper.move(-1000);

}

void loop()
{
  now = millis();
  stepper.runSpeed();
  if ((now - lasttimepub)> 10)
    {
      motor_speed.data = vel_x;
      p.publish( &motor_speed );
      lasttimepub=now;
    }
//  TODO TIMER INTERRUPT FOR PUBLISHER
  nh.spinOnce();
}
