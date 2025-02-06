<<<<<<< HEAD
import pygame
import serial 
import time

pygame.init()
pygame.joystick.init()
baud_rate = 115200
arduino_port = "COM3"

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

try:
    while True:
        pygame.event.pump()
        # Read joystick axis values (scaled between -100 and 100)
        left_stick_x = int(controller.get_axis(0) * 100)
        left_stick_y = int(controller.get_axis(1) * -100)  # Invert Y-axis for natural movement
        right_stick_x = int(controller.get_axis(2) * 100)
        right_stick_y = int(controller.get_axis(3) * -100)
        
        # Read button states (0 or 1)
        a_button = controller.get_button(0)
        b_button = controller.get_button(1)
        x_button = controller.get_button(2)
        y_button = controller.get_button(3)

        data = f"{left_stick_x},{left_stick_y},{right_stick_x},{right_stick_y},{a_button},{b_button},{x_button},{y_button}\n"
        # Send data to Arduino
        ser.write(data.encode('utf-8'))
        print(f"Sent: {data.strip()}")

        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\nStopping script.")
    ser.close()
=======
import pygame
import serial 
import time

pygame.init()
pygame.joystick.init()
baud_rate = 115200
arduino_port = "COM3"

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Allow time for connection to establish
    print(f"Connected to Arduino on {arduino_port}")
except:
    print("Failed to connect to Arduino.")
    exit()

num_joysticks = pygame.joystick.get_count()

try:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print("Controller connected:", controller.get_name())
except:
    print("No controller detected.")
    exit()

try:
    while True:
        pygame.event.pump()
        # Read joystick axis values (scaled between -100 and 100)
        left_stick_x = int(controller.get_axis(0) * 100)
        left_stick_y = int(controller.get_axis(1) * -100)  # Invert Y-axis for natural movement
        right_stick_x = int(controller.get_axis(2) * 100)
        right_stick_y = int(controller.get_axis(3) * -100)
        
        # Read button states (0 or 1)
        a_button = controller.get_button(0)
        b_button = controller.get_button(1)
        x_button = controller.get_button(2)
        y_button = controller.get_button(3)

        data = f"{left_stick_x},{left_stick_y},{right_stick_x},{right_stick_y},{a_button},{b_button},{x_button},{y_button}\n"
        # Send data to Arduino
        ser.write(data.encode('utf-8'))
        print(f"Sent: {data.strip()}")

        time.sleep(0.1) 

except KeyboardInterrupt:
    print("\nStopping script.")
    ser.close()
>>>>>>> d23b2c2524b7daeb934accc1f2a80b11601a4f73
    pygame.quit()