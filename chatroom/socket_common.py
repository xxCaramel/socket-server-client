from dataclasses import dataclass
import socket 


@dataclass
class SocketConf():
    ''' Configuraciones para cliente y servidor
        Opciones:
            PORT:  Numero de puerto de conexión
            SERVER_IP: Número de dirección para conectar/crear
            HEADER: Número de bytes para el header del mensaje
                    Contiene la longitud del mensaje
            FORMAT: Formato en que se codifica la comuniación
            DISCONNECT: Mensaje para señalar fin de conexión
    '''

    PORT: int = 80
    SERVER_IP: str = socket.gethostname()
    HEADER: int = 128
    FORMAT: str = "utf-8"
    DISCONNECT: str = "SCKBR"
    SERVER_ID: str = "SERVER"
        


@dataclass
class ServerConf(SocketConf):
    '''Configuraciones para servidor
        
        MAX_CONN: Número máximo de conecciones
    '''
    MAX_CONN: int = 10
    UPL_FOLD: str = "./uploads/"
   
    
@dataclass
class ClientConf(SocketConf):
    '''Configruaciones para cliente'''
    pass

