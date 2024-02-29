import struct
import time
from millis import Millis
from udp_helper import send_udp_data
from udp_listener import UdpListener
from enum import Enum

class Command(Enum):
    TIMESYNC = 1
    DUMMY = 2
    ACCELEROMETER_READING = 3
    GYROSCOPE_READING = 4
    POSITION_READING = 5


class Sensor:
    def __init__(self, id):
        self.id = id
        self.millis = Millis()
        self.udp_listener = UdpListener(50000, self.time_sync)
        self.address = None
  
    def time_sync(self, data, address):
        payload = struct.unpack("!BB", data)
        if payload[0] == ord('S'):
            self.address = address
            self.time_sync_reply(payload[1])
    
    def time_sync_reply(self, seq):
        reply = struct.pack("<BBBIH", self.id, Command.TIMESYNC.value, seq, self.millis(), 0)
        if self.address is not None:
            send_udp_data(self.address[0], 1234, reply)

    def send_value(self, command, value):
        reply = struct.pack("<BBIfffH", self.id, command, self.millis(), *value, 0)
        if self.address is not None:
            send_udp_data(self.address[0], 1234, reply)


if __name__ == "__main__":
    sensor = Sensor(99)
    while True:
        print("Main thread is running...")
        sensor.send_value(Command.POSITION_READING.value, [1.0, 2.0, 3.0])
        time.sleep(1)
