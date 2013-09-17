# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum
from NetCommunication import NetSocketFun

class RecvAuditDhGenerate(MsgHandleInterface.MsgHandleInterface,object):
    "身份验证成功"
    def __init__(self):
        super(RecvAuditDhGenerate,self).__init__() 
    
    def HandleMsg(self,bufsize,session):
        "请求发送文件"
        msghead = self.packetMsg(MagicNum.MsgTypec.REQFILEBUFFER, 0)
        NetSocketFun.NetSocketSend(session.sockfd,msghead)
       
        
        
