import math
import random
import struct
import time
from millis import Millis
from udp_helper import send_multicast_data
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
        self.multicast_group = "224.0.0.100"
        self.multicast_group_port = 1234
        self.time_sync_port = 50000
        self.udp_listener = UdpListener(self.multicast_group, self.time_sync_port, self.time_sync)
        self.address = None
        
    def time_sync(self, data, address):
        payload = struct.unpack("!BB", data)
        if payload[0] == ord('S'):
            self.address = address
            self.time_sync_reply(payload[1])
    
    def time_sync_reply(self, seq):
        reply = struct.pack("<BBBIH", self.id, Command.TIMESYNC.value, seq, self.millis(), 0)
        if self.address is not None:
            send_multicast_data(self.multicast_group, self.multicast_group_port, reply)

    def send_value(self, command, value):
        reply = struct.pack("<BBIfffH", self.id, command, self.millis(), *value, 0)
        if self.address is not None:
            send_multicast_data(self.multicast_group, self.multicast_group_port, reply)


if __name__ == "__main__":
    sensor = Sensor(99)
    x0 = -0.3
    y0 = 0.0
    r = 0.25
    sim_time = 0.0
    omega = 0.5
    step_time = 0.4
    error = 0.05
    error_rate = 0.005
    x_error = 0.0
    y_error = 0.0

    while True:
        x_error += random.uniform(-error_rate, error_rate)
        y_error += random.uniform(-error_rate, error_rate)
        x_error = min(max(x_error, -error), error)
        y_error = min(max(y_error, -error), error)
        x = x0 + r * math.cos(omega*sim_time) + x_error
        y = y0 + r * math.sin(omega*sim_time) + y_error
        print(f"x: {x}, y: {y}")
        sensor.send_value(Command.POSITION_READING.value, [x, y, 0.0])
        sim_time += step_time
        time.sleep(step_time)
