import time
import os
from usb_serial_reader import USBSerialReader
from hid_output import HIDOutput
from command_processor import CommandProcessor


print("📥 Ready to receive commands over USB Serial...\n")
reader = USBSerialReader()
hid_output = HIDOutput()
processor = CommandProcessor(hid_output)

while True:
    command = reader.read()
    if command:
        processor.execute(command)
    time.sleep(0.01)