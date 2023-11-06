// -->subsrcibe to 'vel_array'
// publish '


// required library
// ROS
//#define USE_USBCON  // MUST BEFORE INCLUDE ROS LIBRARY

#include <ros.h>
#include <rospy_tutorials/Floats.h>
#include <std_msgs/Float64.h>

// Stepper
#include <TMC2130Stepper.h>
#include <AccelStepper.h>



// TMC2130 & encoder set-up
// defines pins numbers
// motor 1/M1
#define EN_PIN_M1    7  // Nano v3:  16 Mega:  38  UNO:  7 //enable (CFG6)
#define DIR_PIN_M1   8  //           19        55        8 //direction
#define STEP_PIN_M1  9  //           18        54        9 //step
#define CS_PIN_M1    10 //           17        64        10//chip select

// initialize TMC2130 driver & encoder
int microstepping = 2;
// M1
TMC2130Stepper TMC2130_M1 = TMC2130Stepper(EN_PIN_M1, DIR_PIN_M1, STEP_PIN_M1, CS_PIN_M1);
AccelStepper stepper_M1(1, STEP_PIN_M1, DIR_PIN_M1); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

// encoder set-up
// defines pins numbers
// encoder 2/M2
#define encoderChA_M1 2
#define encoderChB_M1 3
volatile int lastEncoded_M1 = 0;
volatile long encoderValue_M1 = 0,lastEncoderValue_M1 = 0, encoderPos_M1 = 0,last_pos_M1=0;
long lastencoderValue_M1 = 0;
int lastMSB_M1 = 0;
int lastLSB_M1 = 0;

//must declaration
// ROS
ros::NodeHandle nh;

float vel_x=0.0, vel_y =0.0, vel_stepper_M1=0.0;
float vel_stepper_M1_desired=0.0;
double a = 0.0;

// msgs needed
rospy_tutorials::Floats joy_states;
rospy_tutorials::Floats motors_states; 
std_msgs::Float64 motor_encoder;

ros::Publisher p("motor_encoder", &motor_encoder);


//callback function
void messageCb(const std_msgs::Float64 &msg){
  
  vel_stepper_M1_desired = int(msg.data);
  stepper_M1.setSpeed(vel_stepper_M1_desired);

}
// subscriber for arduino
ros::Subscriber<std_msgs::Float64> s("vel_array", &messageCb);

// timer for publish in fixed rate
unsigned long lastTime,now,lasttimepub;


void setup()
{

  // ROS node/pub/sub
  nh.initNode();
  nh.subscribe(s);
  nh.advertise(p);

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
  stepper_M1.setMaxSpeed(500);
  stepper_M1.setSpeed(0.0);

  //ROS rospy_tutorial_msg
//  motors_states.data_length = 8;
//  motors_states.data = (float *)malloc(sizeof(float)*8);
//  motors_states.data[0] = 0.0;
//  motors_states.data[1] = 0.0;
//  motors_states.data[2] = 0.0;
//  motors_states.data[3] = 0.0;
//  motors_states.data[4] = 0.0;
//  motors_states.data[5] = 0.0;
//  motors_states.data[6] = 0.0;
//  motors_states.data[7] = 0.0;

  // Encoder setup
  // Sets the two pins as Outputs
  //eM1:
  pinMode(encoderChA_M1, INPUT);
  pinMode(encoderChB_M1, INPUT);
  digitalWrite(encoderChA_M1, HIGH); //turn pullup resistor on
  digitalWrite(encoderChB_M1, HIGH); //turn pullup resistor on
  attachInterrupt(digitalPinToInterrupt(encoderChA_M1), updateEncoder_M1, CHANGE); 
  attachInterrupt(digitalPinToInterrupt(encoderChB_M1), updateEncoder_M1, CHANGE);
  
}

void loop()
{
  stepper_M1.runSpeed();

  now = millis();

  if ((now - lasttimepub)> 9) // !!!TEST the MAX HZ
    {
      //encoder algorithm:
//      vel_stepper_M1 = (encoderValue_M1-lastEncoderValue_M1)*100.0/(now - lasttimepub);
//      lastEncoderValue_M1 = encoderValue_M1;
//      motors_states.data[0] = encoderValue_M1;
//      motors_states.data[1] = 0;
//      motors_states.data[2] = 0;
//      motors_states.data[3] = 0;
//      // Or calculate the vel in ROS?
//      motors_states.data[4] = vel_stepper_M1; // unit counts/time
//      motors_states.data[5] = 0;
//      motors_states.data[6] = 0;
//      motors_states.data[7] = 0;

      motor_encoder.data = encoderValue_M1;
      p.publish(&motor_encoder);
      lasttimepub=now;
    }

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
