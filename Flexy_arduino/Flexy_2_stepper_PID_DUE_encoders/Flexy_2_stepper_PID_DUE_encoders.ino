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

// initialize TMC2130 driver & encoder
// NO

// encoder set-up
// defines pins numbers
// encoder 1/M1
#define encoderChA_M1 15
#define encoderChB_M1 14
// encoder 2/M2
#define encoderChA_M2 17
#define encoderChB_M2 16

//encoder M1
volatile int lastEncoded_M1 = 0;
volatile long encoderValue_M1 = 0,lastEncoderValue_M1 = 0, encoderPos_M1 = 0,last_pos_M1=0;
long lastencoderValue_M1 = 0;
int lastMSB_M1 = 0;
int lastLSB_M1 = 0;
//encoder M2
volatile int lastEncoded_M2 = 0;
volatile long encoderValue_M2 = 0,lastEncoderValue_M2 = 0, encoderPos_M2 = 0,last_pos_M2=0;
long lastencoderValue_M2 = 0;
int lastMSB_M2 = 0;
int lastLSB_M2 = 0;

//must declaration
// ROS
ros::NodeHandle nh;

float vel_stepper_M1=0.0, vel_stepper_M2=0.0;
float vel_stepper_M1_desired=0.0;
double a = 0.0;

// msgs needed
std_msgs::Float64 motor_encoder_M1;
std_msgs::Float64 motor_encoder_M2;

ros::Publisher p_M1("motor_encoder_M1", &motor_encoder_M1);
ros::Publisher p_M2("motor_encoder_M2", &motor_encoder_M2);

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
  nh.advertise(p_M1);
  nh.advertise(p_M2);

  delay(1000);

  // Encoder setup
  // Sets the two pins as Outputs
  //eM1:
  pinMode(encoderChA_M1, INPUT);
  pinMode(encoderChB_M1, INPUT);
  digitalWrite(encoderChA_M1, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M1, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M1), updateEncoder_M1, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M1), updateEncoder_M1, CHANGE);
  //eM2:
  pinMode(encoderChA_M2, INPUT);
  pinMode(encoderChB_M2, INPUT);
  digitalWrite(encoderChA_M2, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M2, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M2), updateEncoder_M2, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M2), updateEncoder_M2, CHANGE);
}

void loop()
{

  now = millis();

  if ((now - lasttimepub)> 16) // !!!10 will very likely to fail.
    {

      motor_encoder_M1.data = encoderValue_M1;
      motor_encoder_M2.data = encoderValue_M2;
      p_M1.publish(&motor_encoder_M1);
      p_M2.publish(&motor_encoder_M2);

      lasttimepub=now;
    }

  nh.spinOnce();
}
void updateEncoder_M1(){
  int MSB_M1 = digitalRead(encoderChA_M1); //MSB = most significant bit
  int LSB_M1 = digitalRead(encoderChB_M1); //LSB = least significant bit

  int encoded_M1 = (MSB_M1 << 1) |LSB_M1; //converting the 2 pin value to single number
  int sum_M1  = (lastEncoded_M1 << 2) | encoded_M1; //adding it to the previous encoded value

  if(sum_M1 == 0b1101 || sum_M1 == 0b0100 || sum_M1 == 0b0010 || sum_M1 == 0b1011) encoderValue_M1 --;
  if(sum_M1 == 0b1110 || sum_M1 == 0b0111 || sum_M1 == 0b0001 || sum_M1 == 0b1000) encoderValue_M1 ++;

  lastEncoded_M1 = encoded_M1; //store this value for next time
}
void updateEncoder_M2(){
  int MSB_M2 = digitalRead(encoderChA_M2); //MSB = most significant bit
  int LSB_M2 = digitalRead(encoderChB_M2); //LSB = least significant bit

  int encoded_M2 = (MSB_M2 << 1) |LSB_M2; //converting the 2 pin value to single number
  int sum_M2  = (lastEncoded_M2 << 2) | encoded_M2; //adding it to the previous encoded value

  if(sum_M2 == 0b1101 || sum_M2 == 0b0100 || sum_M2 == 0b0010 || sum_M2 == 0b1011) encoderValue_M2 --;
  if(sum_M2 == 0b1110 || sum_M2 == 0b0111 || sum_M2 == 0b0001 || sum_M2 == 0b1000) encoderValue_M2 ++;

  lastEncoded_M2 = encoded_M2; //store this value for next time
}
