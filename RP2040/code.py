# import time
# import os
# from usb_serial_reader import USBSerialReader
# from hid_output import HIDOutput
# from command_processor import CommandProcessor


# print("📥 Ready to receive commands over USB Serial...\n")
# reader = USBSerialReader()
# hid_output = HIDOutput()
# processor = CommandProcessor(hid_output)

# # Check if the SD card is mounted

# while True:
#     command = reader.read()
#     if command:
#         processor.execute(command)
#     time.sleep(0.01)

import time
import board # type: ignore
from screen import Screen
from key_store import KeyStore
from encoder import RotaryEncoderWithButton
from auth_manager import authenticate
from usb_serial_reader import USBSerialReader
from hid_output import HIDOutput
from command_processor import CommandProcessor


print("📥 Ready to receive commands over USB Serial...\n")
reader = USBSerialReader()
hid_output = HIDOutput()
processor = CommandProcessor(hid_output)

# Encoder setup
encoder = RotaryEncoderWithButton()
tft = Screen()

# Menu State
modes = ["MANUAL","AUTO"]
mode_index = 0
stage = "mode_selection"  # stages: mode_selection, auth, login

# Simulated USB input handler
authenticated = False
login_index = 0
DELAY = 0.1

def draw_mode_screen():
    tft.clear()
    tft.write("Select Mode:", x=10, y=10, identifier="title")
    tft.write(modes[mode_index], x=10, y=30, color=0xFFFF00, identifier="mode")

def draw_auth_screen():
    tft.clear()
    tft.write("Authenticate with key", x=10, y=20, identifier="auth")

def draw_login_screen():
    tft.clear()
    tft.write("Login Page", x=10, y=20, identifier="login")
    domain = list(processor.vault.db.keys())[login_index]
    tft.write(domain, x=10, y=50, identifier="domain")

draw_mode_screen()

while True:
    encoder.update()

    if stage == "mode_selection":
        direction = encoder.get_direction()
        if direction == "CW":
            mode_index = (mode_index + 1) % len(modes)
            tft.update("mode", modes[mode_index])
        elif direction == "CCW":
            mode_index = (mode_index - 1) % len(modes)
            tft.update("mode", modes[mode_index])

        if encoder.was_pressed():
            if modes[mode_index] == "MANUAL":
                stage = "auth"
                draw_auth_screen()
            else:
                stage = "auto"  # Not implemented yet

    elif stage == "auth":
        # Simulated USB command (e.g., "auth 1234")
        print("Waiting for authentication...")
        while(processor.authenticated == False):
            command = reader.read()
            if command:
                processor.execute(command)
        if processor.authenticated:
            tft.write("✅ Auth OK", x=10, y=50, identifier="status")
            stage = "login"
            draw_login_screen()
        else:
            tft.write("❌ Invalid key", x=10, y=50, identifier="status")

  
    elif stage == "login":
        direction = encoder.get_direction()
        if direction == "CW":
            login_index = (login_index + 1) % len(processor.vault.db)
            tft.update("domain", list(processor.vault.db.keys())[login_index])
        elif direction == "CCW":
            login_index = (login_index - 1) % len(processor.vault.db)
            tft.update("domain", list(processor.vault.db.keys())[login_index])

        if encoder.was_pressed():
            domain = list(processor.vault.db.keys())[login_index]
            creds = processor.vault.get(domain)
            print(f"🔑 Credentials for {domain}: {creds}")
            if creds:
                time.sleep(1)
                processor.hid.type_text(creds["username"], delay=DELAY)
                processor.hid.key_strokes("TAB")
                processor.hid.type_text(creds["password"], delay=DELAY)
                processor.hid.key_strokes("ENTER")

    time.sleep(0.05)
