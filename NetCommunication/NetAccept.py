# -*- coding: UTF-8 -*-
import NetAcceptThread
_metaclass_ = type
class NetAccept:
    def __init__(self,view):
        "设置为守护线程"
        self._netaccept = NetAcceptThread.NetAcceptThread(view)
        self._netaccept.setDaemon(True)
        #子线程随父线程结束
        
    def startNetConnect(self):
        "启动线程"
        self._netaccept.start()

    def stopNetConnect(self):
        "关闭线程"
        self._netaccept.stop()
        #self._netaccept.join()
if __name__=='__main__':
    n = NetAccept(1234)
    n.startNetConnect() 