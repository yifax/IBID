#include <SoftwareSerial.h>
SoftwareSerial BT(7,8);

int input1 = 5; // 定义uno的pin 5 向 input1 输出 
int input2 = 6; // 定义uno的pin 6 向 input2 输出
int input3 = 9; // 定义uno的pin 9 向 input3 输出
int input4 = 4; // 定义uno的pin 10 向 input4 输出
int ENA = 10;
int ENB = 11;
int trigs = 13;
int echos = 12;
int A = 100;
int B = 90;

char val;
void setup() {
  //pinMode(13,OUTPUT);
  Serial.begin(9600);
  BT.begin(9600);
}

void loop() {
  if(BT.available()){
    val=BT.read();
    Serial.println(val);
  
  if(val=='1'){
      Serial.println('1');
      forward();
      delay(50);
    }
  else if(val=='0'){
      Serial.println('0');
      pause();
      delay(50);
  }
  else if (val=='2'){
      Serial.println('2');
      turn_left();
      delay(10);
  }
  else if (val=='3'){
      Serial.println('3');
      //turn_right();
      delay(10);
  }
}

 // forward();
}

void pause(){
  digitalWrite(input1,LOW);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,LOW);  
  //delay(50);  //延时0.5秒
}

void back(){ 
  analogWrite(ENA,A);
  analogWrite(ENB,B);
  digitalWrite(input1,LOW);
  digitalWrite(input2,HIGH);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,HIGH);  
  delay(50);    
}

void forward()
{ analogWrite(ENA,A);
  analogWrite(ENB,B);
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,HIGH);
  digitalWrite(input4,LOW);  
 // delay(100);    
}

void turn_left()

 {
  //analogWrite(3,100);
  //analogWrite(11,200);
  
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,HIGH);  

  delay(100);    
}
