# caminho do arquivo: PeerServidor.py
import socket
import threading
import logging

logger = logging.getLogger()

# Classe para implementar o servidor de peers
class PeerServidor:
    def __init__(self, peer_manager, message_router):
        self.peer_manager = peer_manager
        self.message_router = message_router

    def handle_peer_connection(self, conn, addr):
        # Lida com a conexão de um peer
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                if message == 'PING':
                    conn.sendall(b'PONG')
                else:
                    logger.info(f"Mensagem recebida de {addr}: {message}")
        except ConnectionResetError:
            pass
        finally:
            conn.close()

    def start_server(self):
        # Inicia o servidor de peers
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.peer_manager.host, self.peer_manager.port))
        server_socket.listen(5)
        logger.info(f"PeerServidor iniciado em {self.peer_manager.host}:{self.peer_manager.port}")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_peer_connection, args=(conn, addr)).start()
