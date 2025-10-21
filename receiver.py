from microbit import *
import radio

radio.on()
radio.config(group=101)

# Motor A control pins
motor_a_stby = pin14  # Standby (enable motor driver)
motor_a_pwm = pin1   # PWM control for Motor A (speed)
motor_a = pin0   # Init motor A signal
motor_a_dir1 = pin12 # Direction pin 1 for Motor A (AIN1)
motor_a_dir2 = pin13 # Direction pin 2 for Motor A (AIN2)

# Motor B control pins
motor_b_stby = pin14  # Same standby pin for Motor B
motor_b_pwm = pin2    # PWM control for Motor B (speed)
motor_b = pin0   # Init motor B signal
motor_b_dir1 = pin15  # Direction pin 1 for Motor B (BIN1)
motor_b_dir2 = pin16  # Direction pin 2 for Motor B (BIN2)

# Initialize motors as stopped
motor_a_stby.write_digital(1)  # Enable motor driver
motor_b_stby.write_digital(1)  # Enable motor driver
motor_a.write_analog(0)
motor_b.write_analog(0)

# Function to move Motor A forward at full speed
def motor_a_forward():
    motor_a_dir1.write_digital(1)  # Forward direction for Motor A
    motor_a_dir2.write_digital(0)  # Forward direction for Motor A
    motor_a_pwm.write_analog(1023)    # Stop Motor A

# Function to move Motor A backward at full speed
def motor_a_backward():
    motor_a_dir1.write_digital(0)  # Backward direction for Motor A
    motor_a_dir2.write_digital(1)  # Backward direction for Motor A

# Function to stop Motor A
def motor_a_stop():
    motor_a_pwm.write_analog(0)    # Stop Motor A
    motor_a_dir1.write_digital(0)  # No direction
    motor_a_dir2.write_digital(0)  # No direction

# Function to move Motor B forward at full speed
def motor_b_forward():
    motor_b_dir1.write_digital(0)  # Forward direction for Motor B
    motor_b_dir2.write_digital(1)  # Forward direction for Motor B

# Function to move Motor B backward at full speed
def motor_b_backward():
    motor_b_dir1.write_digital(1)  # Backward direction for Motor B
    motor_b_dir2.write_digital(0)  # Backward direction for Motor B

# Function to stop Motor B
def motor_b_stop():
    motor_b_pwm.write_analog(0)    # Stop Motor B
    motor_b_dir1.write_digital(0)  # No direction
    motor_b_dir2.write_digital(0)  # No direction

def control_motor(state):
    # Motor A: Use True to run motor and false to turn it off
    if state:
        motor_b_forward()  # Forward Motor B
        motor_a_forward()  # Forward Motor A
    else:
        motor_a_stop() # Stop Motor A
        motor_b_stop() # Stop Motor B

# Set up servo control on pin3
servo_pin = pin8
servo_pin.set_analog_period(20)

def set_servo_angle(angle):
    pulse_width = 0.5 + (angle / 180.0) * 2.0 
    analog_value = int((pulse_width / 20.0) * 1023)
    servo_pin.write_analog(analog_value)


base_hover_angle = 95
set_servo_angle(base_hover_angle)

controlling_enabled = False

def display_gyro(pitch, roll):
    if abs(pitch) < 200 and abs(roll) < 200:
        display.show(Image("00000:"
                           "00000:"
                           "00900:"
                           "00000:"
                           "00000"))
    elif pitch < -300 and roll < -300:
        display.show(Image.ARROW_NW)
    elif pitch > 300 and roll < -300:
        display.show(Image.ARROW_NE)
    elif pitch < -300 and roll > 300:
        display.show(Image.ARROW_SW)
    elif pitch > 300 and roll > 300:
        display.show(Image.ARROW_SE)
    elif pitch < -300:
        display.show(Image.ARROW_W)
    elif pitch > 300:
        display.show(Image.ARROW_E)
    elif roll < -300:
        display.show(Image.ARROW_N)
    elif roll > 300:
        display.show(Image.ARROW_S)
    else:
        display.clear()

def display_button(roll, button):
    if abs(roll) < 200 and not button == "A" and not button == "B":
        display.show(Image("00000:"
                           "00000:"
                           "00900:"
                           "00000:"
                           "00000"))
    elif roll < -300 and not button == "A" and not button == "B":
        display.show(Image.ARROW_N)
    elif roll < -300 and not button == "A" and button == "B":
        display.show(Image.ARROW_NE)
    elif roll < -300 and button == "A" and not button == "B":
        display.show(Image.ARROW_NW)
    elif roll > 300 and not button == "A" and not button == "B":
        display.show(Image.ARROW_S)
    elif roll > 300 and not button == "A" and button == "B":
        display.show(Image.ARROW_SE)
    elif roll > 300 and button == "A" and not button == "B":
        display.show(Image.ARROW_SW)

def control_motor_speed(roll):
    if roll < -200:  # Tilted North (forward)
        # Map roll from -200 to -1023 to speed 0 to 1023
        speed = min(1023, abs(roll + 200) * 1023 // 823)
        motor_b_dir1.write_digital(0)
        motor_b_dir2.write_digital(1)
        motor_b_pwm.write_analog(speed)
    elif roll > 200:  # Tilted South (backward - Motor B only)
        # Map roll from 200 to 1023 to speed 0 to 1023
        speed = min(1023, (roll - 200) * 1023 // 823)
        motor_b_backward()
        motor_b_pwm.write_analog(speed)
    else:  # Center position (stopped/slow)
        motor_b_stop()

def gyro_modus(pitch, roll):
    global base_hover_angle
    new_angle = base_hover_angle + pitch // 20
    new_angle = max(0, min(180, new_angle))
    set_servo_angle(new_angle)
    control_motor_speed(roll)
    display_gyro(pitch, roll)

def button_modus(roll, button):
    global base_hover_angle
    if button == "A":
        base_hover_angle -= 45  # Decrease angle by 45°
    elif button == "B":
        base_hover_angle += 45  # Increase angle by 45°
    base_hover_angle = max(0, min(180, base_hover_angle))
    set_servo_angle(base_hover_angle)
    control_motor_speed(roll)
    display_button(roll, button)

while True:
    incoming = radio.receive()
    if incoming:
        if incoming == "shutdown":
            display.show("T")
            set_servo_angle(95)
            control_motor(False)
            controlling_enabled = False
        elif incoming == "stop":
            controlling_enabled = False
            motor_b_stop()
            display.show("X")
        elif incoming == "start":
            display.show("O")
            motor_a_forward()
            controlling_enabled = True
        elif controlling_enabled:
            try:
                pitch_str, roll_str, modus_str, button_str = incoming.split(",")
                pitch = int(pitch_str)
                roll = int(roll_str)
                modus = int(modus_str)
                button = str(button_str)
                if modus == 0:
                    gyro_modus(pitch, roll)
                if modus == 1:
                    button_modus(roll, button)
            except:
                display.show(Image.CONFUSED)
    sleep(100)