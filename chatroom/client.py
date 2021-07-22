import socket
import json
import threading
from socket_common import ClientConf as conf
from server_options import SeverOptions 

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
        self.__message_list = []
        self.__file_dir = "./client/"


    @property
    def msglist(self):
        return self.__message_list

    def connect(self):
        ''' Abre la conexión entre cliente servidor'''
        self.__socket_client = socket.socket(
            socket.AF_INET,socket.SOCK_STREAM)
        self.__connect_client()
        client_listen = threading.Thread(target=self.__listen)
        client_listen.start()

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
        self.send_message(conf.DISCONNECT,None)
        self.__connection_set = False

    def __prepare_json(self,payload,dest,group,option):
        payload = {
            "dest":dest,
            "group":group,
            "payload":payload,
            "opt":option
        }

        return json.dumps(payload)

    def __listen(self):

        conn = self.__socket_client
        while self.__connection_set:
            message_head = conn.recv(conf.HEADER).decode(conf.FORMAT)
            if message_head: 
                head = json.loads(message_head)
                if head["opt"] == SeverOptions.FILESN:
                    message_len = head["len"]
                    message = conn.recv(message_len)
                    self.__download_file(message,head["aux"])
                else:
                    try:
                        message_len = head["len"]
                        message = conn.recv(message_len).decode(conf.FORMAT)
                        msg = json.loads(message)
                        self.__message_list.append({"from":msg["from"],"payload":msg["payload"]})
                    except ValueError as err:
                        print(f"[FAILED] Likely incorrect Format or Header\n {err}")
                        self.__connection_set = False

    def send_message(self,payload,dest,group=False,opt=None):
        '''Manda el mensaje al servidor
           Parametros:
                payload: Mensaje para enviar al servidor
            
            Retorna:
                True: si se mando con exito
                False: si no hay conexión

        '''
        
        #Informa a server el len del mensaje antes de mandarlo
        payload = self.__prepare_json(payload,dest,group,opt).encode(conf.FORMAT)
        payload_header = self.__gen_head(len(payload),opt)
        
        if not self.__try_to_send(payload_header,payload):
            print("No conectado")
       
       
    def __gen_head(self,length,opt=None):

        header =  {
            "len":length,
            "opt":opt
        }

        json_header = json.dumps(header).encode(conf.FORMAT)
        padding = conf.HEADER - len(json_header)
        json_header += b' ' * padding

        return json_header

    def __try_to_send(self,header,payload):
        if self.__connection_set:
            self.__socket_client.send(header)
            self.__socket_client.send(payload)
            return True
        else:
            return False
    
    def send_file(self,file_name,dest,group=False):

        head_option = SeverOptions.FILESN
        payload = self.__prepare_json(file_name,dest,group,head_option).encode(conf.FORMAT)
        json_header = self.__gen_head(len(payload))

        if not self.__try_to_send(json_header,payload):
            print("No conectado")
            return False


    def __download_file(self,file,name):
        if not name:
            name = "default"
        try:
            file_name = "{}{}".format(self.__file_dir,name)
            new_file = open(file_name,"wb")
            new_file.write(file)
            new_file.close()
        except:
            print("[Algo paso no se pudo descargar]")

    def __upload_server(self,file):
        file_len = len(file)
        options = SeverOptions.FILEUP

        json_header = self.__gen_head(file_len,options)

        if not self.__try_to_send(json_header,file):
            print("No conectado")

    
    def upload_file(self,file_name):
        try:
            file = open(file_name,"rb")
            file_b = file.read()
            self.__upload_server(file_b)
            file.close()
        except FileNotFoundError:
            return 0