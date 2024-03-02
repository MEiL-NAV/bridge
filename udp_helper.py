import socket

def send_udp_data(target_address, target_port, data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if not isinstance(data, bytes):
            data = bytes(data)
        udp_socket.sendto(data, (target_address, target_port))
    except Exception as e:
        print("Error:", e)
    finally:
        udp_socket.close()

def send_multicast_data(multicast_group, multicast_port, data):
    multicast_address = (multicast_group, multicast_port)
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
        if not isinstance(data, bytes):
            data = bytes(data, 'utf-8')
        multicast_socket.sendto(data, multicast_address)
    except Exception as e:
        print("Error:", e)
    finally:
        multicast_socket.close()

# Example usage:
if __name__ == "__main__":
    TARGET_ADDRESS = '192.168.0.100'
    TARGET_PORT = 12345
    try:
        while True:
            data_to_send = b"Hello, UDP!"
            send_udp_data(TARGET_ADDRESS, TARGET_PORT, data_to_send)
    except KeyboardInterrupt:
        pass
