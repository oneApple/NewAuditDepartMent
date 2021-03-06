# -*- coding: UTF-8 -*-

_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from NetCommunication import NetSocketFun

class RecvFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvFileBuffer,self).__init__() 
        
    def HandleMsg(self,bufsize,session):
        "接收文件块"
        if not session.currentbytes:
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,"开始接收文件(" + session.filename + ") ...")
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)[0]
        session.currentbytes += len(recvbuffer)
        session.file.write(recvbuffer)
        msghead = self.packetMsg(MagicNum.MsgTypec.REQFILEBUFFER, 0)
        NetSocketFun.NetSocketSend(session.sockfd,msghead)
        