# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# You must add a gamepad HID device inside your boot.py file
# in order to use this example.
# See this Learn Guide for details:
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9

import board
import usb_hid
import ibus
import busio


# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
   x = min(in_max, x)
   x = max(in_min, x)
   return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min



class IBUSservo():
   '''Helper class for reading servo values and doind something useful'''
   def __init__(self, gamepad):
      self.gamepad = gamepad
      self.last_x = -9999
      self.last_y = -9999
      self.last_a = -9999
      self.last_b = -9999

   def servo_cb(self, data_arr):
      '''This is the callback function to be called by the IBUS update loop.  data_arr will be an array of PPM values per channel'''
      # Do something useful here
      x = data_arr[0]
      y = data_arr[1]
      a = data_arr[2]
      b = data_arr[3]

      if abs(x - self.last_x)>10 or \
         abs(y - self.last_y)>10 or\
         abs(a - self.last_a)>10 or \
         abs(b - self.last_b)>10:

         self.gamepad.move_joysticks(
               x=range_map(x, 1000, 2000, -127, 127),
               y=range_map(y, 1000, 2000, -127, 127),
               z= range_map(a, 1000, 2000, -127, 127),
               r_z = range_map(b, 1000, 2000, -127, 127),
            )
         self.last_x = x
         self.last_y = y
         self.last_a = a
         self.last_b = b

from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

# Instantiates the UART
uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=ibus.PROTOCOL_GAP)

servo = IBUSservo(gp)
# instantiates the IBUS class and specifies the call back
# the board is conected to the SERVO port in this case
ib = ibus.IBUS(uart, [], servo_cb=servo.servo_cb, do_log=False)
# now run the loop forever, calling servo.servo_cb when new servo values are received
ib.start_loop()




