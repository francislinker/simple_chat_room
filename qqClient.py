import socket
import os
import sys

def main():
    #从命令行输入IP地址和端口号
    if len(sys.argv)<3:
        print('参数错误！')
        return

    address=(sys.argv[1],int(sys.argv[2]))
    #创建 UDP 套接字
    client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #发送消息
    client.sendto('francis'.encode(),address)
    #接收消息
    data,addr=client.recvfrom(1024)
    print(data.decode())


if __name__ == "__main__":
    main()

