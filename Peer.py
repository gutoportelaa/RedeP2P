# caminho do arquivo: Peer.py
import socket
import struct
import asyncio
import logging
import time

MCAST_GRP = '224.0.0.1'  # Usar um endereço de multicast válido
MCAST_PORT = 5007
PEER_PORT = 12345

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Classe para gerenciar os peers na rede P2P
class Peer:
    def __init__(self, nome, host, port, subnet, version="0.0"):
        self.nome = nome
        self.host = host
        self.port = port
        self.subnet = subnet
        self.version = version
        self.peers = {}  # Dicionário de peers conhecidos
        self.connected_peers = {}  # Dicionário de peers conectados
        self.grafo_peers = {}  # Estrutura para armazenar o grafo de peers

        self.peers[self.nome] = f'{self.host}:{self.port}'
        self.connected_peers[self.nome] = f'{self.host}:{self.port}'  # Atualização inicial da lista de peers conectados
        self.atualizar_grafo()
        logger.debug(f"Peer iniciado para {self.nome} em {self.host}:{self.port}")

    def atualizar_grafo(self):
        # Atualiza o grafo de peers
        self.grafo_peers = {}
        for peer in self.peers:
            self.grafo_peers[peer] = [(outro_peer, self.medir_latencia(outro_peer)) for outro_peer in self.peers if outro_peer != peer]
        logger.debug(f"Grafo de peers atualizado: {self.grafo_peers}")

    def medir_latencia(self, peer_name):
        # Mede a latência para um peer específico
        peer_addr = self.peers[peer_name]
        peer_host, peer_port = peer_addr.split(':')
        try:
            start_time = time.time()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((peer_host, int(peer_port)))
            client_socket.sendall(b'PING')
            client_socket.recv(4096)
            end_time = time.time()
            client_socket.close()
            latencia = end_time - start_time
            logger.debug(f"Latência medida para {peer_name}: {latencia}s")
            return latencia
        except Exception as e:
            logger.error(f"Erro ao medir latência para {peer_name}: {e}")
            return float('inf')

    async def send_multicast(self):
        # Envia uma mensagem multicast periodicamente para descobrir peers
        message = 'DISCOVER'
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
                sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Falha ao enviar mensagem multicast: {e}")

    async def receive_multicast(self):
        # Recebe mensagens multicast para descobrir novos peers
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Substitui o bind para usar o endereço de host local e porta
        sock.bind((self.host, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            data, addr = sock.recvfrom(1024)
            if data.decode() == 'DISCOVER' and addr[0] != self.host:
                self.peers[addr[0]] = f'{addr[0]}:{PEER_PORT}'
                self.atualizar_grafo()
                logger.debug(f"Novo peer descoberto: {addr[0]}")

    def notify_entry(self):
        # Notifica a entrada de um peer na rede
        logger.info(f"{self.nome} entrou na rede P2P")

    def notify_exit(self):
        # Notifica a saída de um peer na rede
        logger.info(f"{self.nome} saiu da rede P2P")

    def exibir_perfil(self):
        # Exibe o perfil do peer
        perfil = {
            "Nome": self.nome,
            "Host": self.host,
            "Port": self.port,
            "Subnet": self.subnet,
            "Versão": self.version,
            "Peers Conectados": self.connected_peers,
            "Grafo de Peers": self.grafo_peers
        }
        for chave, valor in perfil.items():
            print(f"{chave}: {valor}")

    def connect_to_peer(self, peer_addr, message='HEARTBEAT'):
        # Conecta a um peer e envia uma mensagem
        try:
            peer_host, peer_port = peer_addr.split(':')
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((peer_host, int(peer_port)))
            client_socket.sendall(message.encode())
            client_socket.close()
            logger.info(f"Conectado ao peer {peer_addr} com mensagem: {message}")
        except Exception as e:
            logger.error(f"Erro ao conectar ao peer {peer_addr}: {e}")

    def buscar_peer_por_nome(self, nome_peer):
        # Busca um peer pelo nome
        return self.peers.get(nome_peer)

    def buscar_peer_por_endereco(self, endereco):
        # Busca um peer pelo endereço
        for nome, addr in self.peers.items():
            if addr == endereco:
                return nome
        return None
