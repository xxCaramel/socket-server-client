import sys
import threading

from chat_client import ChatClient
from server_options import SeverOptions as opt


class App:
    def __init__(self):
        self.__client = None
        self.__connected = False
    

    def __connect(self):
        server = input("[Servidor]  ")
        port = int(input("[Puerto]  "))
        self.__client = ChatClient(server,port)
        self.__client.connect()
        self.__connected = True

    def __options(self):

        while True:
            print("""
                [1] Cambiar nombre
                [2] Mandar Mensaje
                [3] Conectar
                [4] Inbox
                [5] Grupos
                [6] Desconectar
                [7] Salir
            """)
            option = self.__input()
            if self.__connected or (option==3):
                self.__action(option)
            else:
                 print("[Conectarse primero]")

    def __input(self):
        try:
            option = int(input("[>>]"))
            return option
        except ValueError as err:
            print("[Invalido]")

    def __groups(self):
        print("""
            [1] Crear Grupo
            [2] Agregar Usuarios a Grupo
            [3] Eliminar Grupo
        """)

        option = self.__input()
        self.__group_action(option)


    def __action(self,option):
        
        actions = {
            1:self.__change_name,
            2:self.__send,
            3:self.__connect,
            4:self.__get_messages,
            5:self.__groups,
            6:self.__close,
            7:self.__exit,
        }

        f = actions.get(option)
        f()

    def __group_action(self,_opt):
      
        new_group = True
        if _opt != 1:
            new_group = False

        if _opt != None:
            if _opt == 3:
                name = input("[Nombre Grupo] ")
                self.__client.request_delgroup(name)
            else:
                name = input("[Nombre Grupo] ")
                users = input("[Usuarios]\n").split()
                self.__client.request_addgroup(name,users,new_group)


    def __change_name(self):
        new_name = input("[Nickname]  ")
        self.__client.request_nickname(new_name)

    def __send(self):
        whom = input("[Destinatorio] ")
        msg = input("[Mensaje]\n")
        group = input("[Es un grupo](N/s) ").lower()
        if group == "s":
            group = True
        else:
            group = False

        self.__client.send_message(msg,whom,group)

    def __close(self):
        if self.__connected:
            self.__client.close()
            self.__connected = False

    def __get_messages(self):
        messages = self.__client.msglist
        for message in messages:
            print("[{}]".format(message["from"]))
            print("\t",message["payload"])
            print("\n")
        
        input()
    def __exit(self):
        if self.__connected:
            self.__close()
        sys.exit(0)

    def loop(self):
        app = threading.Thread(target=self.__options)
        app.start()




app = App()
app.loop()