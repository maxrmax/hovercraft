from microbit import *
import radio

radio.on()
radio.config(group=169)

controlling = False
modus = 0
counter = 0
shutdown_mode = False

def show_direction_gyro(pitch, roll):
    if abs(pitch) < 200 and abs(roll) < 200:
        display.show(Image("00000:"
                           "00000:"
                           "00900:"
                           "00000:"
                           "00000"))
    elif pitch > 300 and roll < -300:
        display.show(Image.ARROW_NE)
    elif pitch > 300 and roll > 300:
        display.show(Image.ARROW_SE)
    elif pitch < -300 and roll > 300:
        display.show(Image.ARROW_SW)
    elif pitch < -300 and roll < -300:
        display.show(Image.ARROW_NW)
    elif roll < -300:
        display.show(Image.ARROW_N)
    elif pitch > 300:
        display.show(Image.ARROW_E)
    elif roll > 300:
        display.show(Image.ARROW_S)
    elif pitch < -300:
        display.show(Image.ARROW_W)
    else:
        display.clear()

def show_direction_button(roll):
    if abs(roll) < 200 and not button_a.is_pressed() and not button_b.is_pressed():
        display.show(Image("00000:"
                           "00000:"
                           "00900:"
                           "00000:"
                           "00000"))
    elif roll < -300 and not button_a.is_pressed() and not button_b.is_pressed():
        display.show(Image.ARROW_N)
    elif roll < -300 and not button_a.is_pressed() and button_b.is_pressed():
        display.show(Image.ARROW_NE)
    elif roll < -300 and button_a.is_pressed() and not button_b.is_pressed():
        display.show(Image.ARROW_NW)
    elif roll > 300 and not button_a.is_pressed() and not button_b.is_pressed():
        display.show(Image.ARROW_S)
    elif roll > 300 and not button_a.is_pressed() and button_b.is_pressed():
        display.show(Image.ARROW_SE)
    elif roll > 300 and button_a.is_pressed() and not button_b.is_pressed():
        display.show(Image.ARROW_SW)

def send_tilt_commands():
    pitch = accelerometer.get_x()
    roll = accelerometer.get_y()
    radio.send("{},{},{},0".format(pitch, roll, modus))
    show_direction_gyro(pitch, roll)

def send_button_commands():
    pitch = accelerometer.get_x()
    roll = accelerometer.get_y()
    if button_a.is_pressed():
        radio.send("{},{},{},A".format(pitch, roll, modus))
        display.show(Image.ARROW_W)
    elif button_b.is_pressed():
        radio.send("{},{},{},B".format(pitch, roll, modus))
        display.show(Image.ARROW_E)
    else:
        radio.send("{},{},{},0".format(pitch, roll, modus))
    show_direction_button(roll)


def input_gyro():
    global controlling, counter
    if button_a.was_pressed():
        controlling = True
        radio.send("start")
        counter = 0

    if button_b.was_pressed():
        controlling = False
        radio.send("stop")
        display.show("X")

    if button_a.is_pressed() and button_b.is_pressed():
        controlling = False
        radio.send("shutdown")
        display.show("T")
        counter += 1

    if controlling:
        send_tilt_commands()

def input_button():
    global controlling, counter  
    if button_a.was_pressed():
        controlling = True
        radio.send("start")
        counter = 0

    if button_b.was_pressed():
        controlling = True
        radio.send("start")
        counter = 0

    if button_a.is_pressed() and button_b.is_pressed():
        sleep(100)
        if button_a.is_pressed() and button_b.is_pressed():
            controlling = False
            radio.send("shutdown")
            display.show("T")
            counter += 1

    if controlling:
        send_button_commands()

while True:
    if counter == 3:
        counter = 0
        modus = 1 if modus == 0 else 0
        display.show(str(modus))
        sleep(1000)

    if modus == 0:
        input_gyro()
    elif modus == 1:
        input_button()

    sleep(200)
