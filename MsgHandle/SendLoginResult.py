# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from DataBase import CPUserTable, NOUserTable
from NetCommunication import NetSocketFun

class SendLoginResult(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendLoginResult,self).__init__()
    
    def verifyUser(self,name,psw):
        "验证用户名密码的正确性"
        self.__db.Connect()
        _res = self.__db.VerifyNamePsw(name, psw)
        self.__db.CloseCon()
        return _res
    
    def HandleMsg(self,bufsize,session):
        "返回登录结果，并保存用户名"
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        _loginmsg = NetSocketFun.NetUnPackMsgBody(recvmsg)
        session.usertype = _loginmsg[0]
        if _loginmsg[0] == MagicNum.UserTypec.CPUSER:
            self.__db = CPUserTable.CPUserTable()
            showmsg = "内容提供商:" + _loginmsg[1] 
        elif _loginmsg[0] == MagicNum.UserTypec.NOUSER:
            self.__db = NOUserTable.NOUserTable()
            showmsg = "网络运营商:" + _loginmsg[1] 
        _res = self.verifyUser(_loginmsg[1], _loginmsg[2])
        if  _res != False:
            msglist = [session.control.view.username.encode("utf8"),str(_res)]
            msgbody = NetSocketFun.NetPackMsgBody(msglist)
            msghead = self.packetMsg(MagicNum.MsgTypec.LOGINSUCCESS,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
            session.peername = _loginmsg[1]
            showmsg += "登录成功"
        else:
            msghead = self.packetMsg(MagicNum.MsgTypec.LOGINFAIL,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
            showmsg += "登录失败"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
