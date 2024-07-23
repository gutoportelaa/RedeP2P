# caminho do arquivo: Menu.py
import os

# Classe para implementar o menu interativo
class Menu:
    def __init__(self, peer_manager, message_router, load_balancer):
        self.peer_manager = peer_manager
        self.message_router = message_router
        self.load_balancer = load_balancer

    def menu_interativo(self):
        # Exibe o menu interativo e processa as opções escolhidas
        while True:
            print("\nMenu Interativo:")
            print("1. Exibir peers")
            print("2. Enviar mensagem")
            print("3. Roteamento de mensagem")
            print("4. Exibir perfil")
            print("5. Buscar peer por nome")
            print("6. Buscar peer por endereço")
            print("7. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                print(f"Peers conectados: {self.peer_manager.peers}")
            elif opcao == '2':
                peer_destino = input("Digite o nome do peer destino: ")
                mensagem = input("Digite a mensagem: ")
                if peer_destino in self.peer_manager.peers:
                    peer_addr = self.peer_manager.peers[peer_destino]
                    self.peer_manager.connect_to_peer(peer_addr, mensagem)
                else:
                    print("Peer não encontrado.")
            elif opcao == '3':
                nome_peer = input("Digite o nome do peer: ")
                mensagem = input("Digite a mensagem: ")
                if nome_peer in self.peer_manager.peers:
                    self.message_router.route_message(nome_peer, mensagem)
                else:
                    print("Peer não encontrado.")
            elif opcao == '4':
                self.peer_manager.exibir_perfil()
            elif opcao == '5':
                nome_peer = input("Digite o nome do peer: ")
                peer_addr = self.peer_manager.buscar_peer_por_nome(nome_peer)
                if peer_addr:
                    print(f"Endereço do peer {nome_peer}: {peer_addr}")
                else:
                    print("Peer não encontrado.")
            elif opcao == '6':
                endereco = input("Digite o endereço do peer (host:port): ")
                nome_peer = self.peer_manager.buscar_peer_por_endereco(endereco)
                if nome_peer:
                    print(f"Nome do peer com endereço {endereco}: {nome_peer}")
                else:
                    print("Peer não encontrado.")
            elif opcao == '7':
                self.peer_manager.notify_exit()
                print('Saindo da rede P2P.')
                os._exit(0)
            else:
                print("Opção inválida.")
