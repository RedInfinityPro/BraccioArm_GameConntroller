import pygame
import serial 
import time

pygame.init()
pygame.joystick.init()
baud_rate = 115200
arduino_port = "COM3"
Gamecontroller = []

#controllerMapping = {
#    "Xbox One Controller": [["A - 0", "B - 1", "Y - 2", "X - 3", "LB - 4", "RB - 5", "SettignsBTN - 6", "Paused - 7", "LeftStickDown - 8", "RightStickDown - 9"],
#                            ["LeftStick - 0", "LeftStick - 1", "RightStick - 2", "RightStick - 3"]]
#}

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
def arduino_connectionAttempt():
    global ser
    try:
        time.sleep(2)  # Allow time for connection to establish
        print(f"Connected to Arduino on {arduino_port}")
    except:
        print("Failed to connect to Arduino.")
        exit()
arduino_connectionAttempt()

controller = pygame.joystick.get_count()
def controller_connectionAttempt():
    global controller
    num_joysticks = pygame.joystick.get_count()
    try:
        controller = pygame.joystick.Joystick(0)
        controller.init()
        print("Controller connected:", controller.get_name())
    except:
        print("No controller detected.")
        exit()
controller_connectionAttempt()

def apply_deadzone(value, threshold=50):  # Deadzone for stability
    return 0 if abs(value) < threshold else value

prev_data = None
def should_send(new_data):
    global prev_data
    if prev_data is None or abs(int(new_data.split(",")[0]) - int(prev_data.split(",")[0])) > 5:  
        prev_data = new_data
        return True
    return False

def main():
    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    buttonMapping = pygame.joystick.Joystick(event.device_index)
                    Gamecontroller.append(buttonMapping)

            for control in Gamecontroller:
                #print(control.get_name())
                # print stick states between between -360 and 360
                left_stick = [apply_deadzone(int(control.get_axis(0) * 360)), apply_deadzone(int(control.get_axis(1) * -360)), control.get_button(8)]
                right_stick = [apply_deadzone(int(control.get_axis(2) * 360)), apply_deadzone(int(control.get_axis(3) * -360)), control.get_button(9)]
                print(left_stick, right_stick)
                # Send data to Arduino
                data = f"{left_stick[0]},{left_stick[1]},{left_stick[0]},{left_stick[1]}"
                if should_send(data):
                    ser.write(data.encode('utf-8'))
                    print(f"Sent: {data.strip()}")
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping script.")
        ser.close()
        pygame.quit()

if __name__ == "__main__":
    main()