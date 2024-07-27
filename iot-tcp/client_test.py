import socket
import random
import time

HOST = '127.0.0.1'
PORT = 9999


def generate_random_data():
    device_ids = [1, 3, 4, 6, 8, 9]  # Device ID for test
    device_id = random.choice(device_ids)
    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    return device_id, latitude, longitude


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            for _ in range(100):
                device_id, latitude, longitude = generate_random_data()
                message = f"{device_id} {latitude} {longitude}\n"
                s.sendall(message.encode())
                print(f"Sent: {message.strip()}")
                time.sleep(0.1)

    except (socket.error, BrokenPipeError) as e:
        print(f"Socket error occurred: {e}")
        time.sleep(5)


if __name__ == "__main__":
    main()
