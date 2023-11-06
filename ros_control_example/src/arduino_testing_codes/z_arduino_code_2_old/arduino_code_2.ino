#include <ros.h>
#include <rospy_tutorials/Floats.h>
#define encodPinA1      2                       // Quadrature encoder A pin
#define encodPinB1      8                       // Quadrature encoder B pin
#define M1              9                       // PWM outputs to motor driver module
#define M2              10

ros::NodeHandle  nh;

double pos = 0, vel= 0, output = 0, temp=0;
unsigned long lastTime,now,lasttimepub;
volatile long encoderPos = 0,encoderPos_1 = 0,encoderPos_2 = 0,last_pos=0;
int flag=0;
rospy_tutorials::Floats joint_state;

void set_angle_cb( const rospy_tutorials::Floats& cmd_msg){
  output= cmd_msg.data[0]; 
}


ros::Subscriber<rospy_tutorials::Floats> sub("/joints_to_aurdino_2", set_angle_cb);
ros::Publisher pub("/joint_states_from_arduino_2", &joint_state);

void setup(){
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
  pinMode(encodPinA1, INPUT_PULLUP);                  // quadrature encoder input A
  pinMode(encodPinB1, INPUT_PULLUP);                  // quadrature encoder input B
  attachInterrupt(digitalPinToInterrupt(encodPinA1), encoder, RISING);

  TCCR1B = TCCR1B & 0b11111000 | 1;                   // set 31KHz PWM to prevent motor noise  
}

void loop(){
  flag=0;
  encoderPos_1=encoderPos_2;
  flag=1;
  pos = (encoderPos_1*360)/1200 ;
  now = millis();
  int timeChange = (now - lastTime);

  if((now - lasttimepub)> 25){
  	temp = (360.0*1000*(encoderPos_1-last_pos)) /(1200*(now - lastTime));
  	vel =temp;
  	lastTime=now;
  	last_pos=encoderPos_1;

    joint_state.data_length=2;
    joint_state.data[0]=pos;
    joint_state.data[1]=vel;
    pub.publish(&joint_state);
    lasttimepub=now;
  }

  pwmOut(output);
  
  nh.spinOnce();

}

void encoder()  {                                     // pulse and direction, direct port reading to save cycles
  if(digitalRead(encodPinB1)==LOW)   encoderPos ++;
  if(digitalRead(encodPinB1)==HIGH)   encoderPos --;
  if(flag) encoderPos_2=encoderPos;
}

void pwmOut(float out) { 

  if (encoderPos > 600 || encoderPos < -600)
    out=0;                                
  if (out > 0) {
    analogWrite(M2, out);                             // drive motor CW
    analogWrite(M1, 0);
  }
  else {
    analogWrite(M2, 0);
    analogWrite(M1, abs(out));                        // drive motor CCW
  }
}
