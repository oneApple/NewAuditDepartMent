# -*- coding: UTF-8 -*-
import threading, socket, select

import NetThread
from GlobalData import MagicNum, ConfigData

_metaclass_ = type
class NetAcceptThread(threading.Thread):
    def __init__(self,view):
        super(NetAcceptThread,self).__init__()
        self.__runflag = True
        self.__threadlist = []
        self.view = view
        
    def run(self):
        "监听，每当有一个新的连接请求则创建新的线程"
        self._listenfd = socket.socket()
        self._listenfd.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        config = ConfigData.ConfigData()
        _listenAddress = config.GetListenAddress()
        
        try:
            self._listenfd.bind((_listenAddress[0],int(_listenAddress[1])))
        except Exception,e:
            self._listenfd.close();
            return MagicNum.NetAcceptc.BINDERROR
        
        self._listenfd.listen(MagicNum.NetAcceptc.MAXLISTENNUM)
        self._listenfd.setblocking(0)
        _epoll = select.epoll()
        _epoll.register(self._listenfd.fileno(),select.EPOLLIN)
       
        while self.__runflag:
            _events = _epoll.poll()
            for fileno ,event in _events:
                if fileno == self._listenfd.fileno():
                    c,addr = self._listenfd.accept()
                    s = 'Got connect from:' + str(addr) + "\n"
                    th = NetThread.NetThread(c.dup(),self,True)
                    self.__threadlist.append(th)
                    th.start()
                    c.close()
                elif event & select.EPOLLHUP:
                    _epoll.unregister(fileno)
                    print "canont listend"
                    self.__runflag = False
                    break
        self._listenfd.close();
        
    def closeNetThread(self,th):
        "关闭单个线程"
        th.stop()
        #th.join()
        self.__threadlist.remove(th)
            
    def stop(self):
        "关闭所有线程"
        print "stop accpet"
        while self.__threadlist:
            th = self.__threadlist[0]
            self.closeNetThread(th)
        self.__runflag = False
        
        