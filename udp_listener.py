import socket
import struct
import threading
import time

class UdpListener:
    def __init__(self, multicast_address, port, handler, timeout=0.2, buffer_size=1024):
        self.is_running = True
        self.multicast_address = multicast_address
        self.port = port
        self.handler = handler
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        mcast_group = socket.inet_aton(self.multicast_address)
        mreq = struct.pack('4sL', mcast_group, socket.INADDR_ANY)
        self.udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.udp_socket.bind(('', self.port))
        self.udp_socket.settimeout(self.timeout)
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.start()

    def loop(self):
        while self.is_running:
            try:
                data, address = self.udp_socket.recvfrom(self.buffer_size)
                self.handler(data, address)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception as e:
                print("Error:", e)
                continue

    def __del__(self):
        self.is_running = False
        self.loop_thread.join()
        self.udp_socket.close()

# example usage
if __name__ == "__main__":
    MULTICAST_GROUP = "224.0.0.100"
    PORT = 50000
    listener = UdpListener(MULTICAST_GROUP, PORT, lambda data, address: print(f"{address}: {data}"))

    while True:
        print("Main thread is running...")
        time.sleep(1)
