
// required library
// ROS
#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY
#include <ros.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Float32MultiArray.h>
#include <sensor_msgs/JointState.h>
#include <sensor_msgs/Joy.h>
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
#define encoderChA_M1 32
#define encoderChB_M1 33
// motor 2/M2
#define EN_PIN_M2    9  // Nano v3:  16 Mega:  38  UNO:  7 //enable (CFG6)
#define DIR_PIN_M2   7  //           19        55        8 //direction
#define STEP_PIN_M2  8  //           18        54        9 //step
#define CS_PIN_M2    6  //           17        64        10//chip select
#define encoderChA_M2 36
#define encoderChB_M2 37
// motor 3/M3
#define EN_PIN_M3    14  //enable (CFG6)
#define DIR_PIN_M3   16  //direction
#define STEP_PIN_M3  15  //step
#define CS_PIN_M3    17  //chip select
#define encoderChA_M3 40
#define encoderChB_M3 41
// motor 4/M4
#define EN_PIN_M4    18  //enable (CFG6)
#define DIR_PIN_M4   20  //direction
#define STEP_PIN_M4  19  //step
#define CS_PIN_M4    21  //chip select
#define encoderChA_M4 44
#define encoderChB_M4 45
// initialize TMC2130 driver & encoder
int microstepping = 4;
int one_revolution = 200 * microstepping;
const int motorSpeedLinearStage = 50;
// M1
TMC2130Stepper TMC2130_M1 = TMC2130Stepper(EN_PIN_M1, DIR_PIN_M1, STEP_PIN_M1, CS_PIN_M1);
AccelStepper stepper_M1(1, STEP_PIN_M1, DIR_PIN_M1); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
// encoder M1
volatile int lastEncoded_M1 = 0;
volatile long encoderValue_M1 = 0,lastEncoderValue_M1 = 0, encoderPos_M1 = 0,last_pos_M1=0;
long lastencoderValue_M1 = 0;
int lastMSB_M1 = 0;
int lastLSB_M1 = 0;
// M2
TMC2130Stepper TMC2130_M2 = TMC2130Stepper(EN_PIN_M2, DIR_PIN_M2, STEP_PIN_M2, CS_PIN_M2);
AccelStepper stepper_M2(1, STEP_PIN_M2, DIR_PIN_M2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
//encoder M2
volatile int lastEncoded_M2 = 0;
volatile long encoderValue_M2 = 0,lastEncoderValue_M2 = 0, encoderPos_M2 = 0,last_pos_M2=0;
long lastencoderValue_M2 = 0;
int lastMSB_M2 = 0;
int lastLSB_M2 = 0;
// M3
TMC2130Stepper TMC2130_M3 = TMC2130Stepper(EN_PIN_M3, DIR_PIN_M3, STEP_PIN_M3, CS_PIN_M3);
AccelStepper stepper_M3(1, STEP_PIN_M3, DIR_PIN_M3); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
//encoder M3
volatile int lastEncoded_M3 = 0;
volatile long encoderValue_M3 = 0,lastEncoderValue_M3 = 0, encoderPos_M3 = 0,last_pos_M3=0;
long lastencoderValue_M3 = 0;
int lastMSB_M3 = 0;
int lastLSB_M3 = 0;
// M4
TMC2130Stepper TMC2130_M4 = TMC2130Stepper(EN_PIN_M4, DIR_PIN_M4, STEP_PIN_M4, CS_PIN_M4);
AccelStepper stepper_M4(1, STEP_PIN_M4, DIR_PIN_M4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
//encoder M4
volatile int lastEncoded_M4 = 0;
volatile long encoderValue_M4 = 0,lastEncoderValue_M4 = 0, encoderPos_M4 = 0,last_pos_M4=0;
long lastencoderValue_M4 = 0;
int lastMSB_M4 = 0;
int lastLSB_M4 = 0;


//must declaration
// ROS
ros::NodeHandle nh;

float vel_x=0.0, vel_y =0.0, vel_stepper_M1=0.0, vel_stepper_M2=0.0, vel_stepper_M3=0.0, vel_stepper_M4=0.0;
float vel_stepper_M1_desired=0.0, vel_stepper_M2_desired=0.0, vel_stepper_M3_desired=0.0, vel_stepper_M4_desired=0.0;
float joy_left_LR = 0.1, joy_left_UD = 0.0, joy_right_LR = 0.0, joy_right_UD = 0.0;
int button_X = 0, button_O = 0, button_Tri = 0, button_Squ = 0;
double a = 0.0;

// msgs needed
std_msgs::Float32MultiArray motors_states;
rospy_tutorials::Floats joy_states;

sensor_msgs::Joy joy;


ros::Publisher p("encoder_stepper", &motors_states);


//callback function
void messageCb( const rospy_tutorials::Floats &msg){
//  vel_stepper_M1_desired = msg.axes[0];
//  vel_stepper_M2_desired = msg.axes[1];
//  vel_stepper_M3_desired = msg.axes[2];
//  vel_stepper_M3_desired = msg.axes[3];
//  stepper_M1.setMaxSpeed(vel_stepper_M1_desired);
//  stepper_M2.setMaxSpeed(vel_stepper_M2_desired);
//  stepper_M3.setMaxSpeed(vel_stepper_M3_desired);
//  stepper_M4.setMaxSpeed(vel_stepper_M4_desired);
//  stepper.setSpeed(-vel_stepper);
//  joy_left_LR = msg.axes[0];
//  joy_left_UD = msg.axes[1];
//  joy_right_LR = msg.axes[2];
//  joy_right_UD = msg.axes[3];
//  button_X = msg.buttons[0];
//  button_O = msg.buttons[1];
//  button_Tri = msg.buttons[2];
//  button_Squ = msg.buttons[3];
    joy_states = msg;
}
// subscriber for arduino
ros::Subscriber<rospy_tutorials::Floats> s("joy_array", &messageCb);



// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.advertise(p);
  nh.subscribe(s);
  delay(1000);
  // ROS MultiArray declaration **IMPORTANT!!!**
  // SEE: https://web.archive.org/web/20160711134453/http://answers.ros.org/question/10988/use-multiarray-in-rosserial/
  motors_states.layout.dim = (std_msgs::MultiArrayDimension *)
  malloc(sizeof(std_msgs::MultiArrayDimension) * 2);
  motors_states.layout.dim[0].label = "Motors";
  motors_states.layout.dim[0].size = 6;
  motors_states.layout.dim[0].stride = 1*6;
  motors_states.layout.data_offset = 0;
  motors_states.data = (float *)malloc(sizeof(float)*6);
  motors_states.data_length = 6;
  
  
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
  stepper_M1.setSpeed(800);
  //eM1:
  pinMode(encoderChA_M1, INPUT);
  pinMode(encoderChB_M1, INPUT);
  digitalWrite(encoderChA_M1, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M1, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M1), updateEncoder_M1, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M1), updateEncoder_M1, CHANGE);
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
  stepper_M2.setSpeed(800);
  //eM2:
  pinMode(encoderChA_M2, INPUT);
  pinMode(encoderChB_M2, INPUT);
  digitalWrite(encoderChA_M2, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M2, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M2), updateEncoder_M2, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M2), updateEncoder_M2, CHANGE);
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
  stepper_M3.setSpeed(800);
  //eM3:
  pinMode(encoderChA_M3, INPUT);
  pinMode(encoderChB_M3, INPUT);
  digitalWrite(encoderChA_M3, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M3, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M3), updateEncoder_M3, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M3), updateEncoder_M3, CHANGE);
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
  stepper_M4.setSpeed(800);  
  //eM4:
  pinMode(encoderChA_M4, INPUT);
  pinMode(encoderChB_M4, INPUT);
  digitalWrite(encoderChA_M4, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M4, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M4), updateEncoder_M4, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M4), updateEncoder_M4, CHANGE);
}

void loop()
{
  now = millis();
  stepper_M1.runSpeed();
  stepper_M2.runSpeed();
  stepper_M3.runSpeed();
  stepper_M4.runSpeed();

  if ((now - lasttimepub)> 20) // 100 hz is the max
    {
      //encoder algorithm:
//      vel_stepper_M1 = (encoderValue_M1-lastEncoderValue_M1)*100.0/(now - lasttimepub);
//      lastEncoderValue_M1 = encoderValue_M1;
//      
//      vel_stepper_M2 = (encoderValue_M2-lastEncoderValue_M2)*100.0/(now - lasttimepub);
//      lastEncoderValue_M2 = encoderValue_M2;
//      
//      vel_stepper_M3 = (encoderValue_M3-lastEncoderValue_M3)*100.0/(now - lasttimepub);
//      lastEncoderValue_M3 = encoderValue_M3;
//      
//      vel_stepper_M4 = (encoderValue_M4-lastEncoderValue_M4)*100.0/(now - lasttimepub);
//      lastEncoderValue_M4 = encoderValue_M4;
      
      motors_states.data[0] = joy_states.data[0];
      motors_states.data[1] = joy_states.data[1];
      motors_states.data[2] = joy_states.data[2];
      motors_states.data[3] = joy_states.data[3];
      motors_states.data[4] = joy_states.data[4];
      motors_states.data[5] = joy_states.data[5];
      
      p.publish( &motors_states);
      lasttimepub=now;
    }
//  TODO TIMER INTERRUPT FOR PUBLISHER
  nh.spinOnce();
}

void updateEncoder_M1(){
  int MSB_M1 = digitalRead(encoderChA_M1); //MSB = most significant bit
  int LSB_M1 = digitalRead(encoderChB_M1); //LSB = least significant bit

  int encoded_M1 = (MSB_M1 << 1) |LSB_M1; //converting the 2 pin value to single number
  int sum_M1  = (lastEncoded_M1 << 2) | encoded_M1; //adding it to the previous encoded value

  if(sum_M1 == 0b1101 || sum_M1 == 0b0100 || sum_M1 == 0b0010 || sum_M1 == 0b1011) encoderValue_M1 ++;
  if(sum_M1 == 0b1110 || sum_M1 == 0b0111 || sum_M1 == 0b0001 || sum_M1 == 0b1000) encoderValue_M1 --;

  lastEncoded_M1 = encoded_M1; //store this value for next time
}
void updateEncoder_M2(){
  int MSB_M2 = digitalRead(encoderChA_M2); //MSB = most significant bit
  int LSB_M2 = digitalRead(encoderChB_M2); //LSB = least significant bit

  int encoded_M2 = (MSB_M2 << 1) |LSB_M2; //converting the 2 pin value to single number
  int sum_M2  = (lastEncoded_M2 << 2) | encoded_M2; //adding it to the previous encoded value

  if(sum_M2 == 0b1101 || sum_M2 == 0b0100 || sum_M2 == 0b0010 || sum_M2 == 0b1011) encoderValue_M2 ++;
  if(sum_M2 == 0b1110 || sum_M2 == 0b0111 || sum_M2 == 0b0001 || sum_M2 == 0b1000) encoderValue_M2 --;

  lastEncoded_M2 = encoded_M2; //store this value for next time
}
void updateEncoder_M3(){
  int MSB_M3 = digitalRead(encoderChA_M3); //MSB = most significant bit
  int LSB_M3 = digitalRead(encoderChB_M3); //LSB = least significant bit

  int encoded_M3 = (MSB_M3 << 1) |LSB_M3; //converting the 2 pin value to single number
  int sum_M3  = (lastEncoded_M3 << 2) | encoded_M3; //adding it to the previous encoded value

  if(sum_M3 == 0b1101 || sum_M3 == 0b0100 || sum_M3 == 0b0010 || sum_M3 == 0b1011) encoderValue_M3 ++;
  if(sum_M3 == 0b1110 || sum_M3 == 0b0111 || sum_M3 == 0b0001 || sum_M3 == 0b1000) encoderValue_M3 --;

  lastEncoded_M3 = encoded_M3; //store this value for next time
}
void updateEncoder_M4(){
  int MSB_M4 = digitalRead(encoderChA_M4); //MSB = most significant bit
  int LSB_M4 = digitalRead(encoderChB_M4); //LSB = least significant bit

  int encoded_M4 = (MSB_M4 << 1) |LSB_M4; //converting the 2 pin value to single number
  int sum_M4  = (lastEncoded_M4 << 2) | encoded_M4; //adding it to the previous encoded value

  if(sum_M4 == 0b1101 || sum_M4 == 0b0100 || sum_M4 == 0b0010 || sum_M4 == 0b1011) encoderValue_M4 ++;
  if(sum_M4 == 0b1110 || sum_M4 == 0b0111 || sum_M4 == 0b0001 || sum_M4 == 0b1000) encoderValue_M4 --;

  lastEncoded_M4 = encoded_M4; //store this value for next time
}
