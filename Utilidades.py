# caminho do arquivo: Utilidades.py
import hashlib

# Função de hash para distribuir as chaves de forma consistente
def hash_function(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

# Classe para implementação de Consistent Hashing
class ConsistentHashing:
    def __init__(self, replicas=100):
        self.replicas = replicas  # Número de réplicas para cada nó
        self.ring = {}  # Dicionário para armazenar o anel de hash
        self.sorted_keys = []  # Lista de chaves ordenadas

    def add_node(self, node):
        # Adiciona um nó ao anel com múltiplas réplicas
        for i in range(self.replicas):
            key = hash_function(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        # Remove um nó do anel junto com suas réplicas
        for i in range(self.replicas):
            key = hash_function(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        # Obtém o nó responsável por uma chave específica
        if not self.ring:
            return None
        hash_key = hash_function(key)
        index = self._find_index(hash_key)
        return self.ring[self.sorted_keys[index]]

    def _find_index(self, hash_key):
        # Encontra o índice apropriado para uma chave de hash no anel
        low, high = 0, len(self.sorted_keys) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.sorted_keys[mid] >= hash_key:
                high = mid - 1
            else:
                low = mid + 1
        return low % len(self.sorted_keys)
