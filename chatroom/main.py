from server import ServerTCP
from socket_common import SocketConf as conf

server = ServerTCP(server_port=3000)

#conf.HEADER = 256

print("HEADER ",conf.HEADER)
print("PORT ",conf.PORT)
print("FORMAT ",conf.FORMAT)
print("ID ",conf.SERVER_ID)
server.init()