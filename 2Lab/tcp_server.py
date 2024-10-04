import socket

def tcp_server(host='127.0.0.1', port=65433):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Сервер запущен на {host}:{port}")
        
        conn, addr = server_socket.accept()
        with conn:
            print(f"Подключено к {addr}")
            data = conn.recv(1024)
            if data:
                print(f"Получено сообщение: {data.decode()}")
                conn.sendall(data)
                print("Сообщение отправлено обратно клиенту")

if __name__ == "__main__":
    tcp_server()