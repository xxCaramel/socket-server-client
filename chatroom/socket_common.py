from dataclasses import dataclass

@dataclass
class SocketConf:
    ''' Configuraciones para cliente y servidor

        PORT:  Numero de puerto de conexión
        SERVER_IP: Número de dirección para conectar/crear
        HEADER: Número de bytes para el header del mensaje
                Contiene la longitud del mensaje
        FORMAT: Formato en que se codifica la comuniación
        DISCONNECT: Mensaje para señalar fin de conexión

    '''

    PORT: int = 80
    SERVER_IP: str = "127.0.0.1"
    HEADER: int = 64
    FORMAT: str = "utf-8"
    DISCONNECT: str = "SCKBR"
        


@dataclass
class ServerConf(SocketConf):
    '''Configuraciones para servidor
        
        MAX_CONN: Número máximo de conecciones
    '''

    MAX_CONN: int = 5
    pass

@dataclass
class ClientConf(SocketConf):
    '''Configruaciones para cliente'''
    pass

