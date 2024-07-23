# caminho do arquivo: main.py
import threading
import asyncio
from Peer import Peer, PEER_PORT
from MessageRouter import MessageRouter
from BalanceadorDeCarga import BalanceadorDeCarga
from Peer_Servidor import PeerServidor
from Menu import Menu


async def main():
    meu_nome = input("Digite o nome do peer: ")  # Solicita o nome do peer
    meu_host = "127.0.0.1"
    meu_port = PEER_PORT
    subnet = '192.168.0.0/24'

    peer_manager = Peer(meu_nome, meu_host, meu_port, subnet)
    message_router = MessageRouter(peer_manager)
    load_balancer = BalanceadorDeCarga(peer_manager)
    peer_server = PeerServidor(peer_manager, message_router)
    interactive_menu = Menu(peer_manager, message_router, load_balancer)

    # Inicializa o servidor de peers em uma thread separada
    server_thread = threading.Thread(target=peer_server.start_server)
    server_thread.start()

    # Inicializa o balanceador de carga em uma thread separada
    load_balancer_thread = threading.Thread(target=load_balancer.balancear_carga)
    load_balancer_thread.start()

    # Inicializa as tarefas assíncronas para multicast
    multicast_tasks = [
        asyncio.create_task(peer_manager.receive_multicast()),
        asyncio.create_task(peer_manager.send_multicast())
    ]

    # Executa as tarefas multicast em segundo plano
    await asyncio.gather(*multicast_tasks)

if __name__ == "__main__":
    # Inicializa o loop de eventos asyncio em uma thread separada
    asyncio_thread = threading.Thread(target=asyncio.run, args=(main(),))
    asyncio_thread.start()

    # Inicializa o menu interativo na thread principal
    meu_nome = input("Digite o nome do peer: ")  # Solicita o nome do peer (para iniciar o menu corretamente)
    meu_host = "127.0.0.1"
    meu_port = PEER_PORT
    subnet = '192.168.0.0/24'
    
    peer_manager = Peer(meu_nome, meu_host, meu_port, subnet)
    message_router = MessageRouter(peer_manager)
    load_balancer = BalanceadorDeCarga(peer_manager)
    peer_server = PeerServidor(peer_manager, message_router)
    interactive_menu = Menu(peer_manager, message_router, load_balancer)
    
    interactive_menu.menu_interativo()  # Executa o menu interativo na thread principal