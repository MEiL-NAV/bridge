import time

class Millis:
    def __init__(self):
        self.start_time = time.time() * 1000  # Current time in milliseconds since epoch

    def __call__(self, *args, **kwargs):
        current_time = time.time() * 1000
        return int(current_time - self.start_time)

# Example usage:
if __name__ == "__main__":
    millis = Millis()
    time.sleep(0.5)
    print("Milliseconds since creation:", millis())