### Hovercraft Project during the 42 Heilbronn Hackathon - October 2025

#### The Start
It was planned to use the block building on
https://makecode.microbit.org/beta/#editor
to program both microcontroller

During trial and error i figured out that it lacking and moved to python.

As it can translate between block, javascript and python easily there were no issues in using both but either had their own share of limitations.

#### My Rescue
Then i found:
https://python.microbit.org/
which is just a full python suit with documention.

With that website i could just save the project directly as .hex on the microcontroller (per usb cable) without issues.

I have also setup vscode with uflash to be able to do that, but in that step i always need to manually mount the microcontroller first, which i solved with a simple alias that mounts and then runs `uflash project.py`


With both running i shared and easily distributed either way to other people!

#### What you can see - 20.10.25 22:17
You can see both the sender and the receiver code.
I opted for a motion control design which has been fun so far.
The sender displays the direction of the tilt and the receiver will use the received signals to adjust the servo for forward/backward thrust and turning (to be implement properly).

Additionally i thought about implementing thrust as tilt control and Button A as left and Button B as right tomorrow with my teampartner.

#### Day 2 - 21.10.25
Spent a huge chunk of time on getting the servo to work.
As i am writing in python and not using scratch, js or micropython i was stuck figuring out the pin layouts myself and had to trial and error my way through getting both motors and the servo to work.
90 minutes before the deadline i managed to figure out that, despite all documentation, pin 8 is somehow the only pin working analog for the servo when you uflash from .py to the micro:bit.
After that i spent some time finishing up on code and making the forward/backward speed dependend on the forward/backward tilt.

The second mode with button controls was never used in the end.

I had tons of fun!