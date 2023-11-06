//#include <ros.h>
//#include <rospy_tutorials/Floats.h>
#define encoderPin1      2                       // Quadrature encoder A pin
#define encoderPin2      3                       // Quadrature encoder B pin
#define M1              9                       // PWM outputs to motor driver module
#define M2              10

//ros::NodeHandle  nh;

volatile int lastEncoded = 0;
volatile long encoderValue = 0,encoderPos = 0,last_pos=0;;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;

double pos = 0, vel= 0, output = 100, temp=0;
unsigned long lastTime,now,lasttimepub;

//rospy_tutorials::Floats joint_state;

//void set_angle_cb( const rospy_tutorials::Floats& cmd_msg){
//  output= cmd_msg.data[0]; 
//}


//ros::Subscriber<rospy_tutorials::Floats> sub("/joints_to_aurdino_1", set_angle_cb);
//ros::Publisher pub("/joint_states_from_arduino_1", &joint_state);

void setup(){
  
//  nh.initNode();
//  nh.subscribe(sub);
//  nh.advertise(pub);
  Serial.begin (9600);
  pinMode(encoderPin1, INPUT);                        // quadrature encoder input 1
  pinMode(encoderPin2, INPUT);                        // quadrature encoder input 2

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on
  
  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3) 
  attachInterrupt(0, updateEncoder, CHANGE); 
  attachInterrupt(1, updateEncoder, CHANGE);


  
  TCCR1B = TCCR1B & 0b11111000 | 1;                   // set 31KHz PWM to prevent motor noise  
}

void loop(){

  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit


    
  Serial.println(encoderValue);
  delay(100); 
  
  encoderPos=lastencoderValue;
  pos = (encoderPos*360)/2500 ;
  now = millis();
  int timeChange = (now - lastTime);

  if(timeChange>=25 ){
  	temp = (360.0*1000*(encoderPos-last_pos)) /(2500*(now - lastTime));
  	vel =temp;
  	lastTime=now;
  	last_pos=encoderPos;
  }

  pwmOut(output);
  
//  if ((now - lasttimepub)> 25)
//  {
//    joint_state.data_length=2;
//    joint_state.data[0]=pos;
//    joint_state.data[1]=vel;
//    pub.publish(&joint_state);
//    lasttimepub=now;
//  }

//  nh.spinOnce();

}

void updateEncoder(){
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --;

  lastEncoded = encoded; //store this value for next time
}

void pwmOut(float out) { 

  if (encoderPos > 500 || encoderPos < -500)
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


//From bildr article: http://bildr.org/2012/08/rotary-encoder-arduino/
