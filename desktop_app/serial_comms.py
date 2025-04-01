import serial
import serial.tools.list_ports
import time

def find_secure_device():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p.description)
        if "CIRCUITPY" in p.description or "USB-Gerät" in p.description:
            print(f'{p.device} choosen')
            return p.device
    return None

def send_command(command):
    port = find_secure_device()
    if not port:
        print("⚠️ Device not found.")
        return

    try:
        with serial.Serial(port, 115200, timeout=2) as ser:
            time.sleep(1)  # Allow device to reset
            ser.write((command + "\n").encode("utf-8"))
            print(f"📤 Sent: {command}")
    except Exception as e:
        print("💥 Serial error:", e)