import socket

def udp_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP-сервер запущен на {host}:{port}")
        
        while True:
            data, addr = server_socket.recvfrom(1024)
            if data:
                print(f"Получено сообщение от {addr}: {data.decode()}")
                server_socket.sendto(data, addr)
                print("Сообщение отправлено обратно клиенту")

if __name__ == "__main__":
    udp_server()
