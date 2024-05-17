import socket
import time

esp32_ip = "192.168.137.205"
esp32_port = 80

def send_command(ip, angle, sleep):
    print(angle)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, esp32_port))
            s.sendall(angle.encode())
    except ConnectionRefusedError:
        print("Connection refused. Ensure ESP32 server is running.")
    time.sleep(sleep)