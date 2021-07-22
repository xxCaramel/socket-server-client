import sys
from chat_client import ChatClient
import threading

class App:
    def __init__(self):
        self.__client = None
        self.__connected = False
        self.__mensajes = []

    def __connect(self):
        server = input("**Enter server:  ")
        port = int(input("**Enter port number:  "))
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
                [5] Desconectar
                [5] Mandar Archivo
                [6] Salir
            """)
            try:
                option = int(input("[>>] "))
                self.__action(option)
            except ValueError as err:
                print("[Invalido]")

    def __action(self,option):
        
        actions = {
            1:self.__change_name,
            2:self.__send,
            3:self.__connect,
            4:self.__get_messages,
            5:self.__close,
            6:self.__exit,
        }

        f = actions.get(option)
        f()

    def __change_name(self):
        print("Here")
        new_name = input("Nickname:")
        self.__client.request_nickname(new_name)

    def __send(self):
        whom = input("Destinatorio\n")
        msg = input("Messaje:\n")
        group = input("Es un grupo (N/s)").lower()
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
            print("\n")
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