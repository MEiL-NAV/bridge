import socket
import threading
import time

class UdpListener:
    def __init__(self, port, handler, timeout=0.2, buffer_size=1024):
        self.is_running = True
        self.port = port
        self.handler = handler
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    PORT = 50000
    listener = UdpListener(PORT, lambda data, address: print(f"{address}: {data}"))

    while True:
        print("Main thread is running...")
        time.sleep(1)
