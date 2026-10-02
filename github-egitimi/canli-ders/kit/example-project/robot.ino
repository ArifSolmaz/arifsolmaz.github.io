// robot.ino — line-following robot
// Arduino Uno + L298N motor driver + 3 infrared line sensors

int SPEED = 200;       // speed on straights (0-255)
int TURN_SPEED = 120;  // speed in turns
int THRESHOLD = 500;   // sensor threshold: above this counts as the black line

// L298N motor driver pins
const int LEFT_SPEED_PIN = 5;   // ENA (PWM)
const int RIGHT_SPEED_PIN = 6;  // ENB (PWM)
const int LEFT_IN1 = 7;
const int LEFT_IN2 = 8;
const int RIGHT_IN3 = 9;
const int RIGHT_IN4 = 10;

// Line sensors
const int SENSOR_LEFT = A0;
const int SENSOR_CENTER = A1;
const int SENSOR_RIGHT = A2;

void setup() {
  pinMode(LEFT_SPEED_PIN, OUTPUT);   // left motor
  pinMode(RIGHT_SPEED_PIN, OUTPUT);  // right motor
  pinMode(LEFT_IN1, OUTPUT);
  pinMode(LEFT_IN2, OUTPUT);
  pinMode(RIGHT_IN3, OUTPUT);
  pinMode(RIGHT_IN4, OUTPUT);

  // Both motors turn forward
  digitalWrite(LEFT_IN1, HIGH);
  digitalWrite(LEFT_IN2, LOW);
  digitalWrite(RIGHT_IN3, HIGH);
  digitalWrite(RIGHT_IN4, LOW);
}

void loop() {
  bool leftOnLine = analogRead(SENSOR_LEFT) > THRESHOLD;
  bool centerOnLine = analogRead(SENSOR_CENTER) > THRESHOLD;
  bool rightOnLine = analogRead(SENSOR_RIGHT) > THRESHOLD;

  if (leftOnLine) {
    motors(TURN_SPEED / 2, TURN_SPEED);  // line on the left: turn left
  } else if (rightOnLine) {
    motors(TURN_SPEED, TURN_SPEED / 2);  // line on the right: turn right
  } else if (centerOnLine) {
    motors(SPEED, SPEED);                // line in the middle: go straight
  } else {
    motors(0, 0);                        // line lost: stop
  }
}

void motors(int leftSpeed, int rightSpeed) {
  analogWrite(LEFT_SPEED_PIN, leftSpeed);
  analogWrite(RIGHT_SPEED_PIN, rightSpeed);
}
