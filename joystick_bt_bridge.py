#!/usr/bin/python3

from BluetoothHID import BluetoothHIDService

from dbus.mainloop.glib import DBusGMainLoop

import struct
import utils


import pygame





def process_hid(bthid_srv):
        i = 0
        last_x = -9999
        last_y = -9999
        last_a = -9999
        last_b = -9999

        buttons =  0x00  # all buttons off at start, only supporting 8 buttons
        NUM_BUTTONS = 8  # using an 8 bit unsigned char

        while True:
            pygame.event.pump()

            do_send = False # only send message when something changed, otherwise super laggy

            js = pygame.joystick.Joystick(0)
            x =  int(js.get_axis(0) * 127)
            y =  int(js.get_axis(1) * 127)
            a =  int(js.get_axis(2) * 127)
            b =  int(js.get_axis(3) * 127)

            if  abs(x - last_x)>2 or \
                abs(y - last_y)>2 or \
                abs(a - last_a)>2 or \
                abs(b - last_b)>2:
                do_send = True

            
            for i in range(NUM_BUTTONS):
                button_state = int(js.get_button(i))
                if button_state != utils.get_bit(buttons, i):
                    do_send = True
                    if button_state:
                        buttons = utils.set_bit(buttons, i)
                    else:
                        buttons = utils.clear_bit(buttons, i)

            if do_send:
                    state = bytearray()
                    state.extend(struct.pack("B", 0xA1))  # this is an input report
                    state.extend(struct.pack("b", x))  # X-axis between -127 and 127
                    state.extend(struct.pack("b", y))  # Y-axis between -127 and 127
                    state.extend(struct.pack("b", a))  # Y-axis between -127 and 127
                    state.extend(struct.pack("b", b))  # Y-axis between -127 and 127
                    state.extend(struct.pack("B", buttons))  # unsigned char representing 8 buttons
                    bthid_srv.send(state)
                    last_x, last_y, last_a, last_b = x, y, a, b






if __name__ == '__main__':
    pygame.display.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()

    CONTROLLER_MAC = utils.get_bluetooth_mac()

    DBusGMainLoop(set_as_default=True)
    service_record = open("sdp_record_joystick_4axis.xml").read()
    try:
        bthid_srv = BluetoothHIDService(service_record, CONTROLLER_MAC)
        process_hid(bthid_srv)



    finally:
        print("Exit")
