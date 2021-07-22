from client import Client
from socket_common import ClientConf as conf
from server_options import SeverOptions as opt

class ChatClient(Client):

    def __init__(self,server="127.0.0.1",port=8080):
        super().__init__(server_port=port,server_ip=server)
        self.__direct_msg = False
        self.__direct_usr= None
    

    def request_nickname(self,nickname):
        option = opt.CHGID
        super().send_message(nickname,conf.SERVER_ID,False,option)

    
    def request_addgroup(self,group_name,users,new_group=True):
        options = opt.CHGRP
        if not new_group:
            options = opt.ADDGRP

        payload = {"name":group_name,"users":users}
        super().send_message(payload,conf.SERVER_ID,False,options)

    def __open_dm(self,user):
        self.__direct_msg = True
        self.__direct_usr = user

    def __request_online(self):
        option = opt.ALLUSR
        super().send_message("Request",conf.SERVER_ID,False,option)

    def loop(self):
        while True:
            dm = input("Open Chat: ")
            self.__open_dm(dm)
            if self.__direct_msg:
                msg = input("(SEND)")
                super().send_message(msg,self.__direct_usr)