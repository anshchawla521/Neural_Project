
bool clear = false;
String c;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13 , OUTPUT);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c[0] = Serial.read();
    for(int i = buf_length - 1 ; i>=1; i--)
    {
      c[i] = c[i-1];
    }
  }

  if(strcmp(c , "hello") == 0)
  {
    digitalWrite(13 , HIGH);
  }else  if(strcmp(c , "not") == 0)
  {
    digitalWrite(13 , LOW);
  }else{
    
  }

}
