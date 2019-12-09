//slave
#include <SoftwareSerial.h>
SoftwareSerial BT(12,13);

int input1 = 5; // 定义uno的pin 5 向 input1 输出 
int input2 = 6; // 定义uno的pin 6 向 input2 输出
int input3 = 9; // 定义uno的pin 9 向 input3 输出
int input4 = 4; // 定义uno的pin 10 向 input4 输出
int ENA = 10;
int ENB = 11;
int trigs = 13;
int echos = 12;
// PWM 
int A = 100;
int B = 100;

char val;
void setup() {
  Serial.begin(9600);
  BT.begin(9600);
}

void loop() {
  if(BT.available()){
    val=BT.read();
  
    if(val=='f'){
      back();
      delay(100);
    }
    else if(val=='s'){
      pause();
    }
    else if(val=='l'){
      turn_left();
      delay(50);
      pause();
    }
    else if(val=='r'){
      turn_right();
      delay(50);
      pause();
    }
    else if(val=='b'){
      forward();
      delay(100);
    }
  }
 }

void pause(){
  digitalWrite(input1,LOW);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,LOW);  
}

void back(){ 
  analogWrite(ENA,A);
  analogWrite(ENB,B);
  digitalWrite(input1,LOW);
  digitalWrite(input2,HIGH);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,HIGH);  
}

void forward()
{ analogWrite(ENA,A);
  analogWrite(ENB,B);
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,HIGH);
  digitalWrite(input4,LOW);     
}

void turn_left()
{ analogWrite(ENA,0);
  analogWrite(ENB,150);
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,HIGH);
  digitalWrite(input4,LOW);     
}
void turn_right()
{ analogWrite(ENA,150);
  analogWrite(ENB,0);
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,HIGH);
  digitalWrite(input4,LOW);     
}
