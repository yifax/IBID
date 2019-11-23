
//LingShun Lab


int input1 = 5; // 定义uno的pin 5 向 input1 输出 
int input2 = 6; // 定义uno的pin 6 向 input2 输出
int input3 = 9; // 定义uno的pin 9 向 input3 输出
int input4 = 10; // 定义uno的pin 10 向 input4 输出
int trigs = 13;
int echos = 12;
int data;

void setup() {
  //Serial.begin (9600);
  //初始化各IO,模式为OUTPUT 输出模式
  
  pinMode(input1,OUTPUT); // Left
  pinMode(input2,OUTPUT);
  pinMode(input3,OUTPUT); // Right
  pinMode(input4,OUTPUT);
  pinMode(3,OUTPUT);  // EN 1
  pinMode(11,OUTPUT); // EN 2
  pinMode(13,OUTPUT);  // SONAR TRIG
  pinMode(12,INPUT);  // SONAR ECHO
  pinMode(2,INPUT);   // 
  pinMode(A0,INPUT);  // Iris
}

 

void loop() {
  //forward 向前转
  data=analogRead(A0);
  digitalWrite(trigs,LOW);
  delayMicroseconds(2);
  digitalWrite(trigs,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigs,LOW);    //发一个10ms的高脉冲去触发TrigPin
  float distanceF = pulseIn(echos,HIGH); //接收高电平时间
  distanceF = distanceF/58.0; //计算距离
  //Serial.println(data);
  //delay(100);

  if (distanceF>15)
    { pause();
      back();
      pause();
    }
  else
    {
      forward();
    }
}

void pause(){
  digitalWrite(input1,LOW);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,LOW);  
  delay(500);  //延时0.5秒
}

void back(){ 
  analogWrite(3,150);
  analogWrite(11,150);
  digitalWrite(input1,LOW);
  digitalWrite(input2,HIGH);  
  digitalWrite(input3,LOW);
  digitalWrite(input4,HIGH);  
  delay(500);    
}

void forward()
{ analogWrite(3,100);
  analogWrite(11,100);
  digitalWrite(input1,HIGH);
  digitalWrite(input2,LOW);  
  digitalWrite(input3,HIGH);
  digitalWrite(input4,LOW);  
  delay(100);    
}
