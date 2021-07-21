import socket
from socket_common import ClientConf as conf

class Client:

    def __init__(self,server_ip=None,server_port=None):
        '''
        Modulo que permite la conexión de un cliente a un servidor
        mediante sockets. Conexión IP/TCP version IPV4
        '''
        if server_port:
            conf.PORT = server_port
        if server_ip:
            conf.SERVER_IP = server_ip

        self.__socket_client = None
        self.__connection_set = False

    def connect(self):
        ''' Abre la conexión entre cliente servidor'''
        self.__socket_client = socket.socket(
            socket.AF_INET,socket.SOCK_STREAM)
        self.__connect_client()

    def __connect_client(self):

        try:
            self.__socket_client.connect(
                (conf.SERVER_IP,conf.PORT)
                )
            self.__connection_set = True
            print("Connected")
        except OSError as err:
            print(f"[FAILED] {err}")
       
    def close(self):
        '''Cierra la conexión con el servidor mandando el mensaje 
           definido DISCONNECT en socket_common
        '''
        self.send_message(conf.DISCONNECT)

    def send_message(self,payload):
        '''Manda el mensaje al servidor
           Parametros:
                payload: Mensaje para enviar al servidor
            
            Retorna:
                True: si se mando con exito
                False: si no hay conexión

        '''
        if self.__connection_set:
            payload = payload.encode(conf.FORMAT)
            payload_header = str(len(payload)).encode(conf.FORMAT)
            payload_header += b' ' * (conf.HEADER-len(payload_header))
            
            self.__socket_client.send(payload_header)
            self.__socket_client.send(payload)
            return True
        else:
            print("No Connection")
            return False