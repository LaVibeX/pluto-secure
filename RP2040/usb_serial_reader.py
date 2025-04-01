import sys
import supervisor

class USBSerialReader:
    """Reads a line from USB Serial (non-blocking, up to end_char)"""
    def __init__(self):
        self._buffer = ''

    def read(self, end_char='\n', echo=True):
        n = supervisor.runtime.serial_bytes_available
        if n > 0:
            s = sys.stdin.read(n)
            if echo:
                sys.stdout.write(s)
            self._buffer += s
            if s.endswith(end_char):
                command = self._buffer.strip()
                self._buffer = ''
                return command
        return None
