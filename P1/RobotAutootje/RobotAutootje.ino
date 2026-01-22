/*Robot autootje gemaakt door Konrad en Berend V6
 * Arduino Nano en L298N Dual H-bridge motor driver
 */

#define ENA 10 // Motor A speed control pin
#define IN1 9  // Motor A direction control pin 1
#define IN2 8  // Motor A direction control pin 2
#define ENB 5  // Motor B speed control pin
#define IN3 7  // Motor B direction control pin 1
#define IN4 6  // Motor B direction control pin 2

// Function prototypes
void driveMotors(int speedA, int speedB);
void controlMotors(int directionA, int directionB);
void stopMotors();

void setup() {
  // Setting pin modes
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  controlMotors(1, 1); //(L, R)
  driveMotors(75, 75); // Motor A and Motor B run
  
  delay(3000); // Wait for 3 seconds
  
  // First motor runs continuously
  controlMotors(1, 1);
  driveMotors(0, 0); // Motor A runs, Motor B stops
  
  delay(1500); // Wait for 1.5 seconds
  
  // Second motor stops
}

// Sets the speeds of motors A and B
void driveMotors(int speedA, int speedB) {
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
}

// Sets the directions of motors A and B
void controlMotors(int directionA, int directionB) {
  digitalWrite(IN1, directionA);
  digitalWrite(IN2, !directionA);
  digitalWrite(IN3, directionB);
  digitalWrite(IN4, !directionB);
}
