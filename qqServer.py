
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
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#设置端口复用

    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#绑定地址
    
    address = (('0.0.0.0',8888))
    server.bind(address)
    #创建多线程，让子进程负责管理员喊话，父进程和客户端交互
    
    pid = os.fork()
    
    if pid<0:#如果进程创建失败
        print('进程创建失败！')
        return

    elif pid == 0:#子进程的任务
        while True:
            content=input('管理员说话：')
            message="speak 管理员：%s" % content
            server.sendto(message.encode(),address)


    else:#父进程处理客户端的各种请求
        doRequest(server)


#处理客户端请求的函数
def doRequest(server):
    userlist={}#此字典用于存放客户端的名字和地址
    while True:
    #接收来自客户端的消息
        msg,addr = server.recvfrom(1024)
        msglist = msg.decode().split(' ')#拆分数据,以空格为分隔
        if msglist[0] == 'login':#如果是进入聊天室请求
            doLogin(server,userlist,msglist[1],addr)
        elif msglist[0] == 'speak':
            #msglist:['c','name','content']
            content = ' '.join(msglist[2:])#获取完整发送内容
            #发送给其他所有成员
            doChat(server,content,userlist,msglist[1])

        elif msglist[0] == 'quit':
            doQuit(server,msglist[1],userlist)

#客户端退出处理函数
def doQuit(server,name,userlist):
    message = '\n%s 退出了聊天室' %name
    for u in userlist:
        if u!=name:
            server.sendto(message.encode(),userlist[u])
        else:
            server.sendto('exit'.encode(),userlist[name])
        #从存储结构中删除
    del userlist[name]

        
#用于聊天的函数（把内容发送给其他成员）
def doChat(server,content,userlist,name):
    message = '\n%s 说：%s' % (name,content)
    for u in userlist:
        if u!= name:#发给不是自身的所有客户端
            server.sendto(message.encode(),userlist[u])


#列表用字典存储{name,addr}
#进入聊天室请求处理函数
def doLogin(server,userlist,name,addr):
    #判断姓名是否同名
    if (name in userlist) or name == '管理员':#如果列表中已经存在此用户名,或取名为管理员
        server.sendto('该用户已经存在！'.encode(),addr)
        return#函数结束，返回继续接收新的数据

    #同名不存在，发送信号给客户端，运行进入
    server.sendto('OK'.encode(),addr)
    #通知所有人
    message='\n欢迎%s进入聊天室'%name
    for u in userlist:
        server.sendto(message.encode(),userlist[u])#全发
    userlist[name]=addr#加入到存储结构userlist字典中
    print(userlist)


if __name__ == '__main__':
    main()