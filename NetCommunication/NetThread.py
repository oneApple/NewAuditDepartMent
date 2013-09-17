# -*- coding: UTF-8 -*-
import threading ,struct

from GlobalData import CommonData
from MsgHandle import MsgHandleMap
from NetCommunication import NetSocketFun

_metaclass_ = type
class NetThread(threading.Thread):
    "网络通信线程"
    def __init__(self,sock,control,isAccept):
        super(NetThread,self).__init__()
        self.control = control
        self.sockfd = sock
        self.runflag = True
        self.currentbytes = 0
        self.isAccept = isAccept
        
    def run(self):
        "接受消息头之后，得到消息类型，然后选择具体的处理类来处理该消息"
        _MsgHandleMap = MsgHandleMap.MsgHandleMap()
        while self.runflag:
            recvbuffer = NetSocketFun.NetSocketRecv(self.sockfd,struct.calcsize(CommonData.MsgHandlec.MSGHEADTYPE))
            if len(recvbuffer) == 0 or (len(recvbuffer) != struct.calcsize(CommonData.MsgHandlec.MSGHEADTYPE)):
                break
            recvmsghead = struct.unpack(CommonData.MsgHandlec.MSGHEADTYPE,recvbuffer)
            print recvmsghead
            _MsgHandleMap.getMsgHandle(recvmsghead[0]).HandleMsg(recvmsghead[1],self)
        #跳出循环，线程结束，关闭socket
        print "thread close"
        self.sockfd.close()
        #self.control.StopNetConnect()


    def stop(self):
        "关闭该线程"
        self.runflag = False