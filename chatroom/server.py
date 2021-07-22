import socket
import threading
import sys
import json

from socket_common import ServerConf as conf
from server_options import SeverOptions as opt
from server_groups import ServerGroup

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
        self.__groups = []

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
                    if msg["payload"] == conf.DISCONNECT:
                        conn_status = False
                    if msg["opt"] != None:
                        response = self.__check_options(msg,client)
                        if not response: break
                    if msg["group"] == True:
                        print("[GROUP INCOMING]")
                        self.__group_broadcast(client,msg)
                    else:
                        self.__broadcast(msg,client["id"])
                    print("[{}]: {}".format(client["id"],msg["payload"]))
                except ValueError as err:
                    print(f"[FAILED] Likely incorrect Format or Header\n {err}")
                    conn_status = False
                

        print("Closing Client")
        conn.close()
        self.__clients.remove(client)


    def __check_options(self,msg,client):

        print(msg["opt"])

        valid=True
        if msg["opt"] == opt.CHGID:
            self.__change_id(client,msg),
        elif msg["opt"] == opt.CHGRP:
            self.__new_group(client,msg)
        elif msg["opt"] == opt.DELGRP:
            self.__del_group(client,msg)
        else:
            valid=False
        
        if not valid:
            print("[INVALID OPT]")
        
        return True

    def __del_group(self,client,msg):
        
        error_msg = {"dest":client["id"],"payload":"Grupo no borrado"}
        for g in self.__groups:
            if g.admin == client["id"] and g.name == msg["payload"]:
                self.__groups.remove(g)
                error_msg["payload"] = f"Grupo {g.name} Borrado"

        self.__broadcast(error_msg,conf.SERVER_ID)

    def __new_group(self,client,msg):
        
        group = msg["payload"]
        name = group["name"]
        admin = client["id"]
        
        users = group["users"]
        conns = [client]
        for _client in self.__clients:
            for user in users:
                print("[BRUH]",_client["id"],user)
                if _client["id"] == user:
                    print("Added ",user)
                    conns.append(_client)

        
        new_group = ServerGroup(name,admin,conns)
        self.__groups.append(new_group)
        msg = {"dest":client["id"],"payload":"Grupo creado: {}".format(name)}

        self.__broadcast(msg,conf.SERVER_ID)

    def __change_id(self,client,msg):
        available = True
        response = {
            "payload":None,
            "dest":client["id"]
        }
        for _client in self.__clients:
            if _client["id"] == msg["payload"]:
                available  = False

        if  available:
            client["id"] = msg["payload"]
            response["dest"] = client["id"]
            response["payload"]="Nuevo Nombre: {}".format(msg["payload"])
        else:
            response["payload"]="Nickname no disponible"
           

        self.__broadcast(response,conf.SERVER_ID)

    def _new_client(self,name, conn):
        """Crea un nuevo cliente

            Parametros:
                name: identifacion del cliente
                conn: conexión socket del cliente

            Retorna:
                Diccionario con keys: id y conn
        """
        client = {
            "id":str(name),
            "conn":conn
        }
        return client
    
    def __display_clients(self):
        if not self.__clients:
            return
        for client in self.__clients:
            print("[CLIENT]{}".format(client["id"]))

    def __broadcast(self,payload,sender_id,group=False):
        
        payload_msg = {
            "from":sender_id,
            "payload":payload["payload"]

        }

        payload_header, payload_json = self.__encode_message(payload_msg)
    
        dest=None
        for client in self.__clients:
            if client["id"] == payload["dest"]:
                dest = client["conn"]
        
        if dest:
            dest.send(payload_header)
            dest.send(payload_json)
        elif (payload["dest"] == conf.SERVER_ID):
            pass
        else:
            print("No one to send to")
       
    def __encode_message(self,msg):

        payload_json = json.dumps(msg).encode(conf.FORMAT)
        payload_header = str(len(payload_json)).encode(conf.FORMAT)
        payload_header += b' ' * (conf.HEADER-len(payload_header))

        return (payload_header,payload_json)

            

    def __group_broadcast(self,sender,payload):

        payload_msg = {
            "from":sender["id"],
            "payload":payload["payload"]
        }

        payload_header, payload_json = self.__encode_message(payload_msg)

        group = None
        for g in self.__groups:
            print("Group ",g.users)
            if g.name == payload["dest"]:
                group = g.users
        if group:
            for user in group:
                print("[SENDING TO GROUP]")
                print(user["id"],sender["id"])
                if user["id"] != sender["id"]:
                    print("[SEND TO] ",user["id"])
                    user["conn"].send(payload_header)
                    user["conn"].send(payload_json)
                    print("[SEND GROUP DONE]")
                
            


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
