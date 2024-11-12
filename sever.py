import socket
import threading

# Cài đặt địa chỉ và cổng của server
HOST = '0.0.0.0'  # hoặc địa chỉ IP của máy chủ trong mạng nội bộ, ví dụ '192.168.1.5'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Server đang chờ kết nối...")

clients = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                # Gửi dữ liệu đến các client khác
                for c in clients:
                    if c != client_socket:
                        c.send(data.encode('utf-8'))
        except:
            clients.remove(client_socket)
            break

while True:
    client_socket, addr = server.accept()
    print(f"Người chơi kết nối từ {addr}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
