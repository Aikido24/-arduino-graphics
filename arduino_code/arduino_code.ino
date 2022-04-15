#define ledPWM1 5
#define ledPWM2 6
#define in1 A0
#define in2 A1

float lectura, signal1, signal2;
float voltaje1, voltaje2;
int coma1,n,led;
String datos,numero,indice;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(in1,INPUT);
  pinMode(in2,INPUT);
  pinMode(ledPWM1,OUTPUT);
  pinMode(ledPWM2,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  signal1 = analogRead(A0);
  signal2 = analogRead(A1);

  voltaje1 = ((signal1/1023)*5.5);
  voltaje2 = ((signal2/1023)*5.5);

  Serial.print(voltaje1);
  Serial.print(',');
  Serial.print(voltaje2);
  Serial.print('\n');
  delay(100);

  //LEDs PWM

  if(Serial.available()>0){
    datos = Serial.readString();
    coma1 = datos.indexOf(',');

    indice = datos.substring(0,coma1);
    numero = datos.substring(coma1+1);

    led = numero.toInt();
    n = indice.toInt();

    if(n == 1){
      analogWrite(ledPWM1,led);
    }
    if(n==2){
      analogWrite(ledPWM2, led);
    }
    delay(100);
  }
}
