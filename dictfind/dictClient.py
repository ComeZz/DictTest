'''
dict 客户端
功能：根据用户输入，发送请求，得到结果
结构：
    一级界面：注册 登录 退出
    二级界面：查单词 历史记录 注销
'''

from socket import *
from getpass import getpass #运行使用终端

ADDR=('127.0.0.1',8989)
s=socket()
s.connect(ADDR)

username=None

def printfirstPage():
    print("===========")
    print("    1-注册")
    print("    2-登录")
    print("other-退出")
    print("===========")


def printSecondPage():
    print("===========")
    print("    1-查单词")
    print("    2-打印历史记录")
    print("other-注销")
    print("===========")


def Register():
    while True:
        name = input('请输入用户名：')
        pw=getpass()
        pw2=getpass("请再输入一次：")
        if pw!=pw2:
            print("两次密码不一致")
            continue
        if ' ' in name or ' ' in pw:
            print("用户名和密码不能有空格")
        msg="R %s %s"%(name,pw)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='OK':
            print('注册成功')
            global username
            username=name
            return True
        else:
            print("注册失败：",data)
            return False

def Login():
    while True:
        name = input('请输入用户名：')
        pw = getpass()
        if ' ' in name or ' ' in pw:
            print("用户名和密码不能有空格")
        msg = "L %s %s" % (name, pw)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data=='OK':
            print('登录成功')
            global username
            username=name
            return True
        else:
            print("登录失败：",data)
            return False

def LookHistory(name):
    msg='H  %s '%name
    s.send(msg.encode())
    while True:
        data=s.recv(1024).decode()
        if data!='#end':
            print(data)
        else:
            break



def main():
    while True:
        printfirstPage()
        cmd=input("请输入序号：")
        if cmd =='1':
            if not Register():
                continue
        elif cmd=="2":
            if not Login():
                continue
        else:
            #s.send(b'3')
            break

        while True:
            printSecondPage()
            cmd = input("请输入序号：")
            if cmd == '1':
                word=input("请输入需要查找的单词")
                msg='Q  %s  %s'%(username,word)
                s.send(msg.encode())
                data = s.recv(1024).decode()
                print(data)

            elif cmd == "2":
                LookHistory(username)
            else:
                #s.send(b'3')
                break

if __name__ == '__main__':
    main()