import socket

def udp_client(host='127.0.0.1', port=65432, message='Привет!'):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(message.encode(), (host, port))
        data, _ = client_socket.recvfrom(1024)
        print(f"Получен ответ от сервера: {data.decode()}")

if __name__ == "__main__":
    udp_client()
