char c;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(13 , OUTPUT);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c = Serial.read();
    if(c == 'l')
  {
    digitalWrite(13 , HIGH);
  }else  if(c == 'r')
  {
    digitalWrite(13 , LOW);
  }else{
    c = '\0';
  }

  Serial.println(c);
  }

  

}
