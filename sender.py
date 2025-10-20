from microbit import *
import radio

radio.on()
radio.config(group=169)

controlling = False

def show_direction(pitch, roll):
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

def send_tilt_commands():
    pitch = accelerometer.get_x()
    roll = accelerometer.get_y()
    radio.send("{},{}".format(pitch, roll))
    show_direction(pitch, roll)

while True:
    if button_a.was_pressed():
        controlling = True
        radio.send("start")
        display.show("O")

    if button_b.was_pressed():
        controlling = False
        radio.send("stop")
        display.show("X")

    if button_a.is_pressed() and button_b.is_pressed():
        controlling = False
        radio.send("shutdown")
        display.show("T")

    if controlling:
        send_tilt_commands()

    sleep(200)
