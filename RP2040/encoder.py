import board
import rotaryio
import digitalio
import time

class RotaryEncoderWithButton:
    def __init__(self, pin_clk=board.D5, pin_dt=board.D6, pin_sw=board.D9):
        # Rotary encoder setup
        self.encoder = rotaryio.IncrementalEncoder(pin_clk, pin_dt)
        self.last_position = self.encoder.position

        # Button setup
        self.button = digitalio.DigitalInOut(pin_sw)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.last_button = self.button.value

        # State flags
        self.direction = None
        self.button_pressed = False

    def update(self):
        # Handle rotation
        current_position = self.encoder.position
        self.direction = None
        if current_position != self.last_position:
            self.direction = "CW" if current_position > self.last_position else "CCW"
            self.last_position = current_position

        # Handle button
        current_button = self.button.value
        self.button_pressed = False
        if current_button != self.last_button:
            time.sleep(0.01)  # debounce
            if self.button.value == False:
                self.button_pressed = True
            self.last_button = current_button

    def get_direction(self):
        return self.direction

    def was_pressed(self):
        return self.button_pressed

    def get_position(self):
        return self.encoder.position