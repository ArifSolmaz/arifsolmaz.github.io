// robot.ino — çizgi izleyen robot
// Arduino Uno + L298N motor sürücü + 3 kızılötesi çizgi sensörü

int HIZ = 200;         // düz yolda hız (0-255)
int VIRAJ_HIZI = 120;  // virajda hız
int ESIK = 500;        // sensör eşiği: bunun üstü siyah çizgi sayılır

// L298N motor sürücü pinleri
const int SOL_HIZ_PIN = 5;  // ENA (PWM)
const int SAG_HIZ_PIN = 6;  // ENB (PWM)
const int SOL_IN1 = 7;
const int SOL_IN2 = 8;
const int SAG_IN3 = 9;
const int SAG_IN4 = 10;

// Çizgi sensörleri
const int SENSOR_SOL = A0;
const int SENSOR_ORTA = A1;
const int SENSOR_SAG = A2;

void setup() {
  pinMode(SOL_HIZ_PIN, OUTPUT);  // sol motor
  pinMode(SAG_HIZ_PIN, OUTPUT);  // sağ motor
  pinMode(SOL_IN1, OUTPUT);
  pinMode(SOL_IN2, OUTPUT);
  pinMode(SAG_IN3, OUTPUT);
  pinMode(SAG_IN4, OUTPUT);

  // İki motor da ileri yönde döner
  digitalWrite(SOL_IN1, HIGH);
  digitalWrite(SOL_IN2, LOW);
  digitalWrite(SAG_IN3, HIGH);
  digitalWrite(SAG_IN4, LOW);
}

void loop() {
  bool solCizgide = analogRead(SENSOR_SOL) > ESIK;
  bool ortaCizgide = analogRead(SENSOR_ORTA) > ESIK;
  bool sagCizgide = analogRead(SENSOR_SAG) > ESIK;

  if (solCizgide) {
    motorlar(VIRAJ_HIZI / 2, VIRAJ_HIZI);  // çizgi solda: sola dön
  } else if (sagCizgide) {
    motorlar(VIRAJ_HIZI, VIRAJ_HIZI / 2);  // çizgi sağda: sağa dön
  } else if (ortaCizgide) {
    motorlar(HIZ, HIZ);                    // çizgi ortada: düz git
  } else {
    motorlar(0, 0);                        // çizgi kayboldu: dur
  }
}

void motorlar(int solHiz, int sagHiz) {
  analogWrite(SOL_HIZ_PIN, solHiz);
  analogWrite(SAG_HIZ_PIN, sagHiz);
}
