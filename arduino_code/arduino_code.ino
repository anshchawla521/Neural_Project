char c;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dacWrite(25 , 121);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c = Serial.read();
    if(c == 'l')
  {
    dacWrite(25 , 100);
  }else  if(c == 'r')
  {
    dacWrite(25 , 140);
  }else{
    c = '\0';
    dacWrite(25 , 121);
  }

  Serial.println(c);
  }

  

}
