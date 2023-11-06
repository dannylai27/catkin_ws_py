// -->subsrcibe to 'vel_array'
// publish '


// required library
// ROS
#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY

#include <ros.h>
//#include <rospy_tutorials/Floats.h>
#include <std_msgs/Float64.h>


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
// NO

// encoder set-up
// defines pins numbers
// encoder 3/M3
#define encoderChA_M3 19
#define encoderChB_M3 18
// encoder 4/M4
#define encoderChA_M4 21
#define encoderChB_M4 20

//encoder M3
volatile int lastEncoded_M3 = 0;
volatile long encoderValue_M3 = 0,lastEncoderValue_M3 = 0, encoderPos_M3 = 0,last_pos_M3=0;
long lastencoderValue_M3 = 0;
int lastMSB_M3 = 0;
int lastLSB_M3 = 0;
//encoder M4
volatile int lastEncoded_M4 = 0;
volatile long encoderValue_M4 = 0,lastEncoderValue_M4 = 0, encoderPos_M4 = 0,last_pos_M4=0;
long lastencoderValue_M4 = 0;
int lastMSB_M4 = 0;
int lastLSB_M4 = 0;

//must declaration
// ROS
ros::NodeHandle nh;

float vel_stepper_M3=0.0, vel_stepper_M4=0.0;
float vel_stepper_M3_desired=0.0;
double a = 0.0;

// msgs needed
std_msgs::Float64 motor_encoder_M3;
std_msgs::Float64 motor_encoder_M4;

ros::Publisher p_M3("motor_encoder_M3", &motor_encoder_M3);
ros::Publisher p_M4("motor_encoder_M4", &motor_encoder_M4);

//callback function
// no need
// subscriber for arduino
// no need

// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.advertise(p_M3);
  nh.advertise(p_M4);

  delay(1000);

  // Encoder setup
  // Sets the two pins as Outputs
  //eM3:
  pinMode(encoderChA_M3, INPUT);
  pinMode(encoderChB_M3, INPUT);
  digitalWrite(encoderChA_M3, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M3, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M3), updateEncoder_M3, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M3), updateEncoder_M3, CHANGE);
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

  if ((now - lasttimepub)> 16) // !!!10 will very likely to fail.
    {

      motor_encoder_M3.data = encoderValue_M3;
      motor_encoder_M4.data = encoderValue_M4;
      p_M3.publish(&motor_encoder_M3);
      p_M4.publish(&motor_encoder_M4);

      lasttimepub=now;
    }

  nh.spinOnce();
}
void updateEncoder_M3(){
  int MSB_M3 = digitalRead(encoderChA_M3); //MSB = most significant bit
  int LSB_M3 = digitalRead(encoderChB_M3); //LSB = least significant bit

  int encoded_M3 = (MSB_M3 << 1) |LSB_M3; //converting the 2 pin value to single number
  int sum_M3  = (lastEncoded_M3 << 2) | encoded_M3; //adding it to the previous encoded value

  if(sum_M3 == 0b1101 || sum_M3 == 0b0100 || sum_M3 == 0b0010 || sum_M3 == 0b1011) encoderValue_M3 --;
  if(sum_M3 == 0b1110 || sum_M3 == 0b0111 || sum_M3 == 0b0001 || sum_M3 == 0b1000) encoderValue_M3 ++;

  lastEncoded_M3 = encoded_M3; //store this value for next time
}
void updateEncoder_M4(){
  int MSB_M4 = digitalRead(encoderChA_M4); //MSB = most significant bit
  int LSB_M4 = digitalRead(encoderChB_M4); //LSB = least significant bit

  int encoded_M4 = (MSB_M4 << 1) |LSB_M4; //converting the 2 pin value to single number
  int sum_M4  = (lastEncoded_M4 << 2) | encoded_M4; //adding it to the previous encoded value

  if(sum_M4 == 0b1101 || sum_M4 == 0b0100 || sum_M4 == 0b0010 || sum_M4 == 0b1011) encoderValue_M4 --;
  if(sum_M4 == 0b1110 || sum_M4 == 0b0111 || sum_M4 == 0b0001 || sum_M4 == 0b1000) encoderValue_M4 ++;

  lastEncoded_M4 = encoded_M4; //store this value for next time
}
