# encoding: utf-8
# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@ author: Hubery
@ create on: 2018/4/18 16:59
@ file: connecter.py
@ site: 
@ purpose: 网络连接，连接游戏服务器，进行收发包以及加解密操作
"""
import asyncio,logging,time
import struct
import socket
from threading import Thread


def printRecvData(_data, align=8):
    print("pack total length is ", len(_data))
    print("head of pack:")
    xRow = 1
    for i in _data:
        print("0x%02x" % int(i), end=' ')
        if xRow % 6 == 0:
            print("\n")
            break
        xRow += 1

    print("body of pack:")
    xRow = 1
    temp_data = _data[6:]
    for i in temp_data:
        print("0x%02x" % int(i), end=' ')
        if xRow % align == 0:
            print("\n")
            xRow += 1
    print("\n")


def thEventLoop(loop):
    asyncio.set_event_loop(loop)
    print("loop: %s" % loop)
    loop.run_forever()


def get_loop():
    localEventLoop = asyncio.new_event_loop()
    localEventThread = Thread(target=thEventLoop, args=(localEventLoop,))
    localEventThread.start()
    return localEventLoop


def loop_close(loop):
    for task in asyncio.Task.all_tasks():
        print(task.cancel())
    loop.stop()
    print("stop event loop")


class Connecter(asyncio.Protocol):
    def __init__(self, ip, port, on_protocol_handle, on_connect_server):
        self.cur_packet_len = 0
        self.ip = ip
        self.port = port
        self.event_loop = get_loop()
        self.connect_task = None
        self.pack_head_length = 6
        self.connected = False
        self.transport = None
        self.isClose = False
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.on_protocol_handle = on_protocol_handle
        self.on_connect_server = on_connect_server

        self.recvBuffer = b''
        self.recv_index = 1

    async def async_connect_(self):
        # try:
        #     self.socket_.connect((self.ip, self.port))
        # except BaseException:
        #     raise BaseException
            # self.connectCallBack_(False)
            # return
        #       创建协程

        # print("xxxxloop: %s" % self.event_loop)

        coro = self.event_loop.create_connection(lambda: self, self.ip, self.port)
        # print("coro : %s" % coro)
        # 创建任务，绑定回调
        self.connect_task = asyncio.ensure_future(coro)
        self.connect_task.add_done_callback(self.on_connect)

        # 安排任务
        await asyncio.wait(self.connect_task, 5)

    def async_connect(self):
        connect_coro = self.async_connect_()
        asyncio.run_coroutine_threadsafe(connect_coro, self.event_loop)

    def on_connect(self, future):
        if future.done():
            con_exception = future.exception()
            if None != con_exception:
                print("error: %s" % con_exception)
            else:
                print("is connected here...")
                self.on_connect_server()
        elif future.cancelled():
            print(u"--> 不能调用，出了问题")
            pass

    def connection_made(self, transport):
        self.connected = True
        self.transport = transport

    def connection_close(self):
        self.connect_task.cancel()

    def send_protocol(self, data):
        if self.isClose:
            return

        self.transport.write(data)  # self.test_check_data()

    def test_check_data(self, data):
        num = struct.unpack("<h", bytes(data[4: 6]))[0]
        if num == 1000:
            # data = data[:len(data) - 1]
            print("1000 data: %s" % data)
        print("send data: ")
        printRecvData(data)

    def data_received(self, data):
        if len(data) > 0:
            self.recvBuffer = data

            body_length = None
            protocol_num = None

            read_packet_is_0_state = False

            while not self.isClose:
                recv_buffer_len = len(self.recvBuffer)

                #  self.cur_packet_len当前读着的包的长度
                #  如果是0说明正在读包头. 读完包头的数据，如果发现包体长度是0的话, 说明此包结构体是空的，需要直接退出，不读此包
                if self.cur_packet_len == 0:
                    if read_packet_is_0_state:
                        break

                    if recv_buffer_len < self.pack_head_length:
                        break
                    flag = self.recvBuffer[0: 2]
                    if flag != b'QS':
                        break
                    self.cur_packet_len = struct.unpack("<h", bytes(self.recvBuffer[2: 4]))[0]
                    body_length = self.cur_packet_len
                    protocol_num = struct.unpack("<h", bytes(self.recvBuffer[4: 6]))[0]
                    # print("---------------",protocol_num)
                    # if protocol_num == 5013:
                    #     print(u"读包头：--> 当前数据：%s flag: %s, 包体长度: %s, 协议号： %s" % (self.recvBuffer, flag, self.cur_packet_len, protocol_num))
                    if body_length is 0:
                        read_packet_is_0_state = True

                #   读包体
                else:
                    if recv_buffer_len < self.cur_packet_len:
                        break
                    # 包长度不含包头，因此包体数据为 self.pack_head_length - self.cur_packet_len
                    body_data = self.recvBuffer[self.pack_head_length: self.pack_head_length + self.cur_packet_len]
                    # 读完一个包, 作用：释放内存, 重置当前包的数据，以便下次收包使用
                    self.recvBuffer = self.recvBuffer[self.pack_head_length + self.cur_packet_len:]
                    self.cur_packet_len = 0

                    if protocol_num is not None:
                        #   转发数据做处理
                        self.on_protocol_handle(protocol_num, body_data)


        else:
            print(u"---> 没有数据进来...")

    #   连接中断标志
    def connection_lost(self, exc):
        print(u"---> 与服务器链接已断开...")
        self.connected = False
        self.isClose = True

if __name__ == '__main__':
    import time
    def qs_protocol():
        print("test...")

    def on_connect_server():
        print("xxxxx")

    for i in range(2):
        conn = Connecter("192.168.1.28", 9037, qs_protocol, on_connect_server)
        conn.async_connect()
        while not conn.connected:
            time.sleep(0.01)
        if conn.transport:
            conn.transport.write(bytes('test', encoding='utf-8'))
            conn.transport.write(
                b'test to recv data')
            #conn.transport.write(b'QS\x1c\x00\xf4\x03\t\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x0b\x00\x00\x001234567890')
        else:
            print("no transport.")

