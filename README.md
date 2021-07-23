# Conexión de Cliente - Servidor mediante Sockets
## Juan Pablo Carvajal

IE0217: Proyecto

# ServerTCP

Crea un servidor IP/TCP (IPV4). Acepta conexiónes hasta un maximo definido

Opciones:

    PORT: Puerto de conexion
    SERVER_IP: Dirección ip del grupo
    HEADER: Tamañano del header
    FORMAT: Formato
    DISCONNECT: Señal de terminación
    SERVER_ID: ID del servidor
    MAX_CONN: Maximos de conneciones
    UPL_FOLD: str = Folder de archivos

## ServerOptions

Opciones para mandar con el mensaje/header al servidor para diferentes funciones

    CHGRP:  Crear grupo
    ADDGRP: Agregar usuarios a grupo
    CHGID:  Cambiar id del cliente
    DELGRP: Borra grupo
    FILESN: Mandar archivo
    FILEUP: Subir archivo
    
## ServerGroups

Clase que crea un grupo de connecions de usuarios con funcionalidad para agregar usuarios extras

# Client

Conecta un cliente a un servidor IP/TCP (IPV4).

Opciones
    DIR: A donde se 'bajan' los archivos


## ChatClient

Hereda de la clase cliente y agrega funciones como:

    request_nickname()
    request_addgroup()
    request_delgroup()