# caminho do arquivo: hybrid_routing.py
import random
import logging

logger = logging.getLogger()

# Classe para representar um nó no Skip Graph
class SkipGraphNode:
    def __init__(self, id, levels):
        self.id = id  # Identificador do nó
        self.levels = levels  # Número de níveis no Skip Graph
        self.forward = [None] * levels  # Lista de ponteiros para frente
        self.backward = [None] * levels  # Lista de ponteiros para trás

# Classe para implementar o Skip Graph
class SkipGraph:
    def __init__(self, max_levels):
        self.max_levels = max_levels  # Número máximo de níveis no Skip Graph
        self.head = SkipGraphNode(None, max_levels)  # Nó cabeça do Skip Graph

    def insert(self, node):
        update = [None] * self.max_levels
        x = self.head

        # Encontrar a posição correta para o novo nó
        for i in reversed(range(self.max_levels)):
            while x.forward[i] and x.forward[i].id < node.id:
                x = x.forward[i]
            update[i] = x

        # Inserir o novo nó nos níveis apropriados
        for i in range(node.levels):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
            if node.forward[i]:
                node.forward[i].backward[i] = node
            node.backward[i] = update[i]
            logger.debug(f"Node {node.id} inserted at level {i}")

    def search(self, id):
        x = self.head
        for i in reversed(range(self.max_levels)):
            while x.forward[i] and x.forward[i].id < id:
                x = x.forward[i]
        x = x.forward[0]
        if x and x.id == id:
            logger.debug(f"Node {id} found")
            return x
        logger.debug(f"Node {id} not found")
        return None

# Classe para implementar a rede de SuperPeers
class SuperPeerNetwork:
    def __init__(self):
        self.super_peers = {}  # Dicionário para armazenar super peers e seus peers

    def add_super_peer(self, super_peer, peers):
        self.super_peers[super_peer] = peers

    def get_peer(self, key):
        # Seleciona um super peer aleatoriamente e busca no seu conjunto de peers
        super_peer = random.choice(list(self.super_peers.keys()))
        peers = self.super_peers[super_peer]
        return random.choice(peers)

# Classe para implementar o roteamento híbrido
class HybridRouting:
    def __init__(self, consistent_hashing, skip_graph, super_peer_network):
        self.consistent_hashing = consistent_hashing
        self.skip_graph = skip_graph
        self.super_peer_network = super_peer_network

    def find_data(self, key):
        # Usar Consistent Hashing para encontrar o nó que possui os dados
        node = self.consistent_hashing.get_node(key)
        if node:
            logger.debug(f"Data for key {key} found at node {node}")
        else:
            logger.debug(f"Data for key {key} not found in Consistent Hashing")
        return node

    def find_peer(self, id):
        # Usar Skip Graph para buscar o peer pelo ID
        node = self.skip_graph.search(id)
        if node:
            logger.debug(f"Peer {id} found in Skip Graph")
        else:
            # Se não encontrado no Skip Graph, usar SuperPeer Network
            node = self.super_peer_network.get_peer(id)
            logger.debug(f"Peer {id} found in Super Peer Network")
        return node
