'''
dict 服务端
功能：业务逻辑处理
模型：多进程tcp并发
'''
from  dictfind.DictDB import *
from socket import *
from  multiprocessing import Process
import signal,sys,time

ADDR=('127.0.0.1',8989)

myDB=dictDB(database='DicDB')

def do_register(c,name,pw):
    if myDB.RegisterUser(name,pw):
        c.send(b'OK')
    else:
        c.send(b'Err')


def do_SeekWord(c,name,word):
    result= myDB.LookupWord(name,word)
    if not result:
        c.send(b'No Word')
    else:
        msg='%s  :  %s'%(result[0],result[1])
        c.send(msg.encode())


def do_Login(c,name,pw):
    if myDB.Login(name,pw):
        c.send(b'OK')
    else:
        c.send(b'Err')

def CheckHist(c,name):
    result=myDB.LookupHis(name)
    if not result:
        c.send(b'No History')
    else:
        for i in range(len(result)):
            msg='%s  :  %s'%(result[i][0],result[i][1])
            c.send(msg.encode())
            time.sleep(0.1)
        c.send(b'#end')




#接受客户端请求，分配处理函数
def handle(c):
    while True:
        data=c.recv(1024)
        if not data:
            break
        print(c.getpeername(),data.decode())

        result=data.decode().split()

        if result[0]=='R':
            do_register(c,result[1],result[2])
        elif result[0]=='Q':
            do_SeekWord(c,result[1],result[2])
        elif result[0]=='L':
            do_Login(c,result[1],result[2])
        elif result[0] == 'H':
            CheckHist(c, result[1])

    c.close()

def main():
    s=socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    print('监听端口：8989，等待客户端链接...')

    while True:
        try:
            connfd,addr=s.accept()
            print('connect :',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue
        #为客户端创建紫禁城
        p=Process(target=handle,args=(connfd,))
        p.daemon=True #父进程退出时子进程自动退出
        p.start()


if __name__ == '__main__':
    main()

