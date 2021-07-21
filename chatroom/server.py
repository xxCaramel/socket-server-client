import socket
import threading
import sys
import json

from socket_common import ServerConf as conf

class ServerTCP():
    '''
    Modulo que da metodos para crear un servidor IP/TCP que acepta
    conexiones IPV4. Opcionalmente se configura mediante socket_common.
    '''

    def __init__(self,server_port = None, server_ip = None):
        '''Parametros:
            server_port (int): Puerto del Servidor (default:80)
            server_ip   (str): Dirección del servidor (default:127.0.0.1)
        '''

        self.__clients = []

        if server_port:
            conf.PORT = server_port
        if server_ip:
            conf.SERVER_IP = server_ip

        self.__server_socket = socket.socket(
            socket.AF_INET,socket.SOCK_STREAM
        )

        #Libera server_ip despues de cerrar
        self.__server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


    def __bind_socket(self):
        """Falla si SERVER_IP o PORT estan en uso"""
        try:
            self.__server_socket.bind(
            (conf.SERVER_IP,conf.PORT)
        )
        except OSError as err:
            print(f"[FAILED] {err}")
            sys.exit()

    
    def __handle_client(self,client):

        new_conn_msg = "[CONNECTED] {}".format(client["id"])
        #self.__broadcast(new_conn_msg)
        print(new_conn_msg)
        
        conn = client["conn"]
        conn_status = True
        while conn_status:
            message_head = conn.recv(conf.HEADER).decode(conf.FORMAT)
            if message_head: # Asegurar que no este vacio
                try:
                    message_len = int(message_head)
                    message = conn.recv(message_len).decode(conf.FORMAT)
                    msg = json.loads(message)
                    if message == conf.DISCONNECT:
                        conn_status = False
                    else:
                        print("[{}]: {}".format(client["id"],msg["payload"]))
                except ValueError as err:
                    print(f"[FAILED] Likely incorrect Format or Header\n {err}")
                    conn_status = False

        print("Closing Client")
        conn.close()

    def _new_client(self,name, conn):
        """Crea un nuevo cliente

            Parametros:
                name: identifacion del cliente
                conn: conexión socket del cliente

            Retorna:
                Diccionario con keys: id y conn
        """
        client = {
            "id":name,
            "conn":conn
        }
        return client
    
    def __display_clients(self):
        if not self.__clients:
            return
        for client in self.__clients:
            print("[CLIENT]{}".format(client["id"]))

    def __broadcast(self,message):
        for client in self.__clients:
            client["conn"].send(message.encode(conf.FORMAT))

    def init(self):
        '''Inicializa sevidor con los parametros definidos
           Crea un thread por cliente
        '''
        self.__bind_socket()
        print("[STARTED] {}:{}".format(conf.SERVER_IP,conf.PORT))
        self.__server_socket.listen(conf.MAX_CONN)

        while True:
            conn, addr = self.__server_socket.accept()
            client = self._new_client(addr[1],conn)
            self.__clients.append(client)
            client_t = threading.Thread(target=self.__handle_client,args=(client,))
            client_t.start()
