import socket
import threading


class RecvDataThread(threading.Thread):
    def setSource(self, clientSocket):
        self.clientSocket = clientSocket

    def terminate(self):
        self.running = False

    def DataProcess(self, data):
        '''
        接收到的数据的格式为: '+10+00231+1100'
        第一个数字10表示label为10
        第二个数字00231表示售出的重量为23.1g
        第三个数字1100表示售出的总价为11.00元
        '''
        if len(data) != 32:
            print('error! length of data is not 32!')
            return
        elif data[0] != '+' or data[2] != '+' or data[7] != '+' or data[12] != '+' or data[17] != '+' or data[22] != '+' or data[27] != '+':
            print('error! data format is wrong!')
            return
        else:
            data = data.split('+')
            # 将label转换成商品名字
            try:
                if data[1] == '1':
                    mode = 'charge'
                elif data[1] == '2':
                    mode = 'discharge'
                else:
                    mode = 'none'

                v_in = str(int(data[2])/100)
                i_in = str(int(data[3])/100)
                v_out = str(int(data[4])/100)
                i_out = str(int(data[5])/100)
                v_b = str(int(data[6])/100)
                i_b = str(int(data[7])/100)
                with open('.\\data.txt', 'w') as f:
                    f.write('mode:'+mode+'\nv_in:'+v_in+'\ni_in:'+i_in+'\nv_out:'+v_out+'\ni_out:'+i_out+'\nv_b:'+v_b+'\ni_b:'+i_b)
            except Exception as e:
                print(e)

    def run(self):
        # 对每个tcp连接都建立到数据库的连接
        self.running = True

        while (self.running):
            try:
                dataReceived = str(self.clientSocket.recv(1024))[2:-1]
                if dataReceived != '':
                    print("\nmessage from client: %s" % str(dataReceived))

                    self.DataProcess(dataReceived)
                # 收到空表示连接已断开
                else:
                    print("connection close")
                    self.running = False
                    self.clientSocket.close()
            # 出现异常
            except Exception as e:
                print(e)
                print("exception occurred, connection close")
                self.running = False
                self.clientSocket.close()


def main():
    # 创建服务器tcp套接字
    tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # (host，port)
    tcpServerSocket.bind(("", 12345))
    tcpServerSocket.listen(5)

    tcpClientSocket = None
    serverOnUse = False

    # 循环等待连接
    for i in range(1):
        print("waiting for client connection.")
        tcpClientSocket, clientIp = tcpServerSocket.accept()
        print("new client connected: %s" % str(clientIp))

        recvDataThread = RecvDataThread()
        recvDataThread.setSource(tcpClientSocket)

        recvDataThread.start()
        recvDataThread.join()

    tcpServerSocket.close()


main()
