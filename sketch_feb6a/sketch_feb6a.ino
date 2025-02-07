#include <Servo.h>
#include <Braccio.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

int x;
#define SMOOTHING_FACTOR 0.7

int smoothValue(int newValue, int oldValue) {
  return (SMOOTHING_FACTOR * oldValue) + ((1 - SMOOTHING_FACTOR) * newValue);
}

void setup() {
  Braccio.begin();
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available())
    ;
  x = Serial.readString().toInt();
  Serial.print(x + 1);
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read input from Python
    int values[8];

    int i = 0;
    char *token = strtok(const_cast<char *>(data.c_str()), ",");
    while (token != NULL && i < 8) {
      values[i++] = atoi(token);
      token = strtok(NULL, ",");
    }
    int baseAngle = map(values[0], -100, 100, 0, 180);
    static int smoothedBaseAngle = baseAngle/2; // Store last known position
    smoothedBaseAngle = smoothValue(baseAngle, smoothedBaseAngle);

    Braccio.ServoMovement(10,         baseAngle, 0, 0, 0, 0,  0);
  }
}