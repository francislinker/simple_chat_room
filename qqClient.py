import socket
import os
import sys

def main():
    #从命令行输入IP地址和端口号
    if len(sys.argv)<3:
        print('参数错误！')
        return

    address = (sys.argv[1],int(sys.argv[2]))
    #创建 UDP 套接字
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #接收用户输入，包装后发送给服务器
    while True:
        name = input('请输入姓名：')
        message = 'login ' + name#此处加入标记
        client.sendto(message.encode(),address)
        data,addr = client.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已经进入聊天室...')
            break

        else:#不允许进入
            #打印不允许进入的原因
            print(data.decode())

        #创建进程
    pid = os.fork()
    if pid<0:
        sys.exit('创建进程失败！')

    elif pid == 0:
        sendmsg(client,name,address)

    else:
        recvmsg(client)

def sendmsg(client,name,address):
    #发送消息给服务器，服务器群发给所有客户端
    while True:
        content=input('请发言（输入quit 退出）：')
        if content == 'quit':
            message =  'quit ' + name
            client.sendto(message.encode(),address)
            sys.exit('已退出聊天室')#子进程退出

        #包装消息
        message = 'speak %s %s' % (name,content)
        client.sendto(message.encode(),address)
    

def recvmsg(client):
    while True:
        message,addr = client.recvfrom(1024)
        if message.decode() == 'exit':#如果收到服务器此消息，父进程退出
            os._exit(0)
        #因为print覆盖了之前的input界面，在这里重新输出一遍
        print(message.decode()+'\n请发言（quit退出）：',end='')

if __name__ == "__main__":
    main()

