import board
import busio
import displayio
import terminalio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label

# Configuración SPI
SPI = busio.SPI(clock=board.D13, MOSI=board.D11)
CS_PIN = board.D12
DC_PIN = board.D10
RST_PIN = board.D8

class Screen:
    def __init__(self, spi=SPI, cs_pin=CS_PIN, dc_pin=DC_PIN, rst_pin=RST_PIN,
                 width=160, height=160, rotation=270, colstart=0, rowstart=0):
        # Liberar cualquier display previo
        displayio.release_displays()

        # Configure the SPI bus
        display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=rst_pin)

        # Initialize the ST7735R display
        self.display = ST7735R(
            display_bus,
            width=width,
            height=height,
            rotation=rotation,
            colstart=colstart,
            rowstart=rowstart,
            bgr=True
        )

        # Create a group to manage display content
        self.splash = displayio.Group()
        self.display.root_group = self.splash

        # Dictionary to store text labels
        self.text_labels = {}

    def clear(self):
        """Clears the screen by removing all elements from the group."""
        self.splash = displayio.Group()
        self.display.root_group = self.splash
        self.text_labels.clear()

    def write(self, text, x=0, y=0, color=0xFFFFFF, background_color=None, scale=1, identifier=None):
        """
        Displays the provided text on the screen at position (x, y).

        :param text: Text to display.
        :param x: Horizontal position of the text.
        :param y: Vertical position of the text.
        :param color: Text color in hexadecimal format (default: white).
        :param background_color: Background color in hexadecimal format (default: None).
        :param scale: Text scale (size).
        :param identifier: Unique identifier for the text label.
        """
        text_area = label.Label(
            terminalio.FONT,
            text=text,
            color=color,
            background_color=background_color,
            scale=scale,
            x=x,
            y=y
        )
        self.splash.append(text_area)
        if identifier:
            self.text_labels[identifier] = text_area

    def update(self, identifier, new_text):
        """
        Updates the text of an existing label identified by 'identifier'.

        :param identifier: Unique identifier of the text label to update.
        :param new_text: New text to display.
        """
        if identifier in self.text_labels:
            self.text_labels[identifier].text = new_text
        else:
            raise ValueError(f"No text label found with identifier '{identifier}'.")

    def remove(self, identifier):
        """
        Removes the text label identified by 'identifier' from the display.

        :param identifier: Unique identifier of the text label to remove.
        """
        if identifier in self.text_labels:
            text_area = self.text_labels.pop(identifier)
            self.splash.remove(text_area)
        else:
            raise ValueError(f"No text label found with identifier '{identifier}'.")
