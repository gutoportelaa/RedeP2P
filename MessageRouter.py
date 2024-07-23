# caminho do arquivo: message_router.py
import logging

logger = logging.getLogger()

# Classe para gerenciar o roteamento de mensagens entre peers
class MessageRouter:
    def __init__(self, peer_manager):
        self.peer_manager = peer_manager

    def route_message(self, peer_name, message):
        # Roteia a mensagem para o peer especificado pelo nome
        if peer_name in self.peer_manager.peers:
            peer_addr = self.peer_manager.peers[peer_name]
            self.peer_manager.connect_to_peer(peer_addr, message)
        else:
            logger.error(f"Peer {peer_name} não encontrado")
