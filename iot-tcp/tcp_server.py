
import socket
import time

from celery_conf import locations_task


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    server_socket.settimeout(60)  # 60 saniye timeout

    print("TCP Server listening on port 9999")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode('utf-8').strip()
                try:
                    device_id, latitude, longitude = decoded_data.split()
                    latitude = float(latitude)
                    longitude = float(longitude)
                    # kuyruğa ekle
                    locations_task.delay(device_id, latitude, longitude)
                    print("Data added to the queue")
                    print("Data :", decoded_data)
                except ValueError as e:
                    print(f"Error processing data: {e}")

            client_socket.close()
        except (socket.timeout, socket.error) as e:
            print(f"Socket error occurred: {e}")

            time.sleep(5)


if __name__ == "__main__":
    start_server()
