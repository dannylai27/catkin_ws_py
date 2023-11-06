
// required library
// ROS
#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY
#include <ros.h>
#include <rospy_tutorials/Floats.h>
#include <std_msgs/Float32MultiArray.h>

// Stepper
#include <TMC2130Stepper.h>
#include <AccelStepper.h>



// encoder set-up
// defines pins numbers
// encoder 2/M2
#define encoderChA_M1 15
#define encoderChB_M1 14
// encoder 2/M2
#define encoderChA_M2 17
#define encoderChB_M2 16
// encoder 3/M3
#define encoderChA_M3 19
#define encoderChB_M3 18
// encoder 4/M4
#define encoderChA_M4 21
#define encoderChB_M4 20
// initialize TMC2130 driver & encoder
// encoder M1
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

float vel_x=0.0, vel_y =0.0, vel_stepper_M1=0.0, vel_stepper_M2=0.0, vel_stepper_M3=0.0, vel_stepper_M4=0.0;
int button_X = 0, button_O = 0, button_Tri = 0, button_Squ = 0;
double a = 0.0;

// msgs needed
rospy_tutorials::Floats test_states; //TO TEST: Floats or Float32MultiArray...
//test_states.data_length = 0;
std_msgs::Float32MultiArray motors_states;
ros::Publisher p("encoder_stepper", &motors_states);

// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.advertise(p);
  delay(1000);

  // ROS MultiArray declaration **IMPORTANT!!!**
  // SEE: https://web.archive.org/web/20160711134453/http://answers.ros.org/question/10988/use-multiarray-in-rosserial/
  motors_states.layout.dim = (std_msgs::MultiArrayDimension *)
  malloc(sizeof(std_msgs::MultiArrayDimension) * 2);
  motors_states.layout.dim[0].label = "Motors";
  motors_states.layout.dim[0].size = 8;
  motors_states.layout.dim[0].stride = 1*8;
  motors_states.layout.data_offset = 0;
  motors_states.data = (float *)malloc(sizeof(float)*8);
  motors_states.data_length = 8;
  
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

  if ((now - lasttimepub)> 20) // !!!TEST the MAX HZ
    {
      //encoder algorithm:
      vel_stepper_M1 = (encoderValue_M1-lastEncoderValue_M1)*100.0/(now - lasttimepub);
      lastEncoderValue_M1 = encoderValue_M1;
      
      vel_stepper_M2 = (encoderValue_M2-lastEncoderValue_M2)*100.0/(now - lasttimepub);
      lastEncoderValue_M2 = encoderValue_M2;
      
      vel_stepper_M3 = (encoderValue_M3-lastEncoderValue_M3)*100.0/(now - lasttimepub);
      lastEncoderValue_M3 = encoderValue_M3;
      
      vel_stepper_M4 = (encoderValue_M4-lastEncoderValue_M4)*100.0/(now - lasttimepub);
      lastEncoderValue_M4 = encoderValue_M4;
      
      motors_states.data[0] = encoderValue_M1;
      motors_states.data[1] = encoderValue_M2;
      motors_states.data[2] = encoderValue_M3;
      motors_states.data[3] = encoderValue_M4;
      motors_states.data[4] = vel_stepper_M1; // unit counts/time
      motors_states.data[5] = vel_stepper_M2;
      motors_states.data[6] = vel_stepper_M3;
      motors_states.data[7] = vel_stepper_M4;


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
