# -*- coding: UTF-8 -*-
import socket, struct

import NetThread
from GlobalData import CommonData, MagicNum
from NetCommunication import NetSocketFun

_metaclass_ = type
class NetConnect:
    def __init__(self,view):
        self.__Sockfd = socket.socket()
    
    def ChangeView(self,view):
        self.__view = view    
        
    def ReqAuditReturn(self,filename,cparams):
        "请求审核" 
        self.filename = filename
        self.cparams = cparams
        msglist = [filename[-filename[::-1].index("/"):].encode("utf-8")]
        _msgbody = NetSocketFun.NetPackMsgBody(msglist)
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQAUDITRETURN,len(_msgbody) )
        NetSocketFun.NetSocketSend(self.__Sockfd,_msghead + _msgbody)
        
        import wx
        from wx.lib.pubsub  import Publisher
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,["请求审核返回文件(" + msglist[0] + ")",False])
        
    def StartNetConnect(self,ip,port):
        "连接服务器并开启网络线程"
        try:
            self.__Sockfd.connect((ip,int(port)))
        except:
            return MagicNum.NetConnectc.NOTCONNECT
        self.__netThread = NetThread.NetThread(self.__Sockfd.dup(),self,False)
        self.__netThread.start()
        
    def StopNetConnect(self):
        "发送关闭消息并关闭网络线程"
        #self.__netThread.join()
        #放在主线程主执行
        pass
        
if __name__=='__main__':
    n = NetConnect(1234)
    n.StartNetConnect()