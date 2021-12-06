Remixed from [EmuBTHID](https://github.com/Alkaid-Benetnash/EmuBTHID)

HID service record from [Bluetooth GPIO Joystick for Raspberry Pi](https://github.com/Heerkog/HIDpi)


Install 

pygame
python-dbus


circuitpython-ibus
adafruit_bus_device
adafruit_hid

** contents of boot.py


Test joystick:
jstest --normal /dev/input/js0



sudo nano /usr/lib/systemd/system/bluetooth.service

[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/lib/bluetooth/bluetoothd -P input


sudo systemctl daemon-reload



