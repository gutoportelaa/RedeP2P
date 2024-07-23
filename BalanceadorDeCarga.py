# caminho do arquivo: BalanceadorDeCarga.py
import time
import random
import logging
from Utilidades import ConsistentHashing
from Hybrid_Routing import SkipGraph, SkipGraphNode, SuperPeerNetwork, HybridRouting

logger = logging.getLogger()

# Classe para implementar o balanceador de carga
class BalanceadorDeCarga:
    def __init__(self, peer_manager):
        self.peer_manager = peer_manager
        self.consistent_hashing = ConsistentHashing()  # Instância de Consistent Hashing
        self.skip_graph = SkipGraph(max_levels=5)  # Instância de Skip Graph
        self.super_peer_network = SuperPeerNetwork()  # Instância de Super Peer Network
        self.hybrid_routing = HybridRouting(self.consistent_hashing, self.skip_graph, self.super_peer_network)  # Instância de roteamento híbrido

        # Adiciona os peers ao Consistent Hashing, Skip Graph e Super Peer Network
        for peer in self.peer_manager.peers.values():
            self.consistent_hashing.add_node(peer)
            self.skip_graph.insert(SkipGraphNode(peer, levels=5))
            self.super_peer_network.add_super_peer(peer, [peer])

    def add_peer(self, peer):
        # Adiciona um peer ao Consistent Hashing, Skip Graph e Super Peer Network
        self.consistent_hashing.add_node(peer)
        self.skip_graph.insert(SkipGraphNode(peer, levels=5))
        self.super_peer_network.add_super_peer(peer, [peer])
        logger.info(f"Peer {peer} adicionado ao hash ring, skip graph e super peer network")

    def remove_peer(self, peer):
        # Remove um peer do Consistent Hashing
        self.consistent_hashing.remove_node(peer)
        # Remoção do Skip Graph e Super Peer Network não implementada para simplificação
        logger.info(f"Peer {peer} removido do hash ring")

    def balancear_carga(self):
        # Executa o balanceamento de carga periodicamente
        while True:
            if len(self.peer_manager.peers) > 10:  # Threshold para iniciar Gossip Protocol
                self._gossip_protocol()
            time.sleep(10)

    def _gossip_protocol(self):
        # Implementa o Gossip Protocol para disseminar a informação
        logger.info("Iniciando Gossip Protocol para balanceamento de carga")
        for _ in range(len(self.peer_manager.peers) // 2):  # Número de iterações para disseminar a informação
            peer = random.choice(list(self.peer_manager.peers.values()))
            self._enviar_mensagem_gossip(peer)

    def _enviar_mensagem_gossip(self, peer):
        # Envia uma mensagem de "Gossip" para outro peer
        try:
            self.peer_manager.connect_to_peer(peer, message="GOSSIP")
            logger.info(f"Mensagem de Gossip enviada para {peer}")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem de Gossip para {peer}: {e}")

    def find_data(self, key):
        # Utiliza o roteamento híbrido para encontrar dados
        return self.hybrid_routing.find_data(key)

    def find_peer(self, id):
        # Utiliza o roteamento híbrido para encontrar um peer
        return self.hybrid_routing.find_peer(id)
