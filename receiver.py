from microbit import *
import radio

radio.on()
radio.config(group=169)

# Set up servo control on pin2
servo_pin = pin2

def set_servo_angle(angle):
    pulse_width = int(500 + (angle / 180) * 2000)
    servo_pin.set_analog_period_microseconds(20000)
    analog_value = int(pulse_width / 20000 * 1023)
    servo_pin.write_analog(analog_value)

base_hover_angle = 90
set_servo_angle(base_hover_angle)

controlling_enabled = False  # Start disabled until "start" is received

def show_direction(pitch, roll):
    if abs(pitch) < 200 and abs(roll) < 200:
        display.clear()
        display.set_pixel(2, 2, 5)  # Bright center dot
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

while True:
    incoming = radio.receive()
    if incoming:
        if incoming == "shutdown":
            display.show("T")
            set_servo_angle(0)
            controlling_enabled = False

        elif incoming == "stop":
            controlling_enabled = False
            display.show("X")

        elif incoming == "start":
            controlling_enabled = True
            display.show("O")

        elif controlling_enabled:
            try:
                pitch_str, roll_str = incoming.split(",")
                pitch = int(pitch_str)
                roll = int(roll_str)

                show_direction(pitch, roll)

                # Adjust servo angle based on pitchfrom microbit import *
import radio

radio.on()
radio.config(group=169)

# Set up servo control on pin2
servo_pin = pin2

def set_servo_angle(angle):
    pulse_width = int(500 + (angle / 180) * 2000)
    servo_pin.set_analog_period_microseconds(20000)
    analog_value = int(pulse_width / 20000 * 1023)
    servo_pin.write_analog(analog_value)

base_hover_angle = 90
set_servo_angle(base_hover_angle)

controlling_enabled = False  # Start disabled until "start" is received

while True:
    incoming = radio.receive()
    if incoming:
        if incoming == "shutdown":
            display.show("T")
            set_servo_angle(0)
            controlling_enabled = False

        elif incoming == "stop":
            controlling_enabled = False
            display.show("X")

        elif incoming == "start":
            controlling_enabled = True
            display.show("O")

        elif controlling_enabled:
            try:
                pitch_str, roll_str = incoming.split(",")
                pitch = int(pitch_str)
                roll = int(roll_str)

                # Mirror the same arrow logic as on the sender
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

                # Update servo angle
                new_angle = base_hover_angle + pitch // 2
                new_angle = max(0, min(180, new_angle))
                set_servo_angle(new_angle)

            except:
                display.show(Image.CONFUSED)

    sleep(100)

                new_angle = base_hover_angle + pitch // 2
                new_angle = max(0, min(180, new_angle))
                set_servo_angle(new_angle)

            except:
                display.show(Image.CONFUSED)

    sleep(100)
