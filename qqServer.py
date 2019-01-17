"""
名称：网络聊天室
环境：Python 3.5
技术：socket, fork
"""

import socket
import os
import sys

#创建网络连接
def main():
    #创建 UDP 套接字
    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#设置端口复用

    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#绑定地址
    
    address=(('0.0.0.0',8888))
    server.bind(address)
    #创建多线程，让子进程负责管理员喊话，父进程和客户端交互
    
    pid = os.fork()
    
    if pid<0:#如果进程创建失败
        print('进程创建失败！')
        return

    elif pid==0:
        print('我是负责管理员喊话的进程')

    else:#父进程处理客户端的各种请求
        doRequest(server)


#处理客户端请求的函数
def doRequest(server):
    #接收来自客户端的消息
    data,addr=server.recvfrom(1024)
    print(data.decode())

    #向客户端发送消息
    server.sendto('服务器已收到'.encode(),addr)




if __name__ == '__main__':
    main()