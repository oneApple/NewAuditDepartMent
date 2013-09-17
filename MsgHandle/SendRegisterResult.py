# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from DataBase import CPUserTable, NOUserTable
from NetCommunication import NetSocketFun

class SendRegisterResult(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendRegisterResult,self).__init__()
    
    def verifyUser(self,name):
        "验证该用户是否已经被注册"
        self.__db.Connect()
        _res = self.__db.searchUser(name)
        self.__db.CloseCon()
        return not _res
    
    def addNewCPUser(self,value):
        "添加新用户"
        self.__db.Connect()
        self.__db.AddNewUser(value)
        self.__db.CloseCon()
    
    def HandleMsg(self,bufsize,session):
        "返回注册信息并保存用户名"
        _recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        _loginmsg = _recvmsg.split(CommonData.MsgHandlec.PADDING) + [MagicNum.CPUserTablec.UNACCEPT]
        if len(_loginmsg) == 6:
            self.__db = CPUserTable.CPUserTable()
        elif len(_loginmsg) == 4:
            self.__db = NOUserTable.NOUserTable()
            
        if self.verifyUser(_loginmsg[0]) == False:
            restype = MagicNum.MsgTypec.REGISTERFAIL
            msghead = self.packetMsg(restype,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
        else:
            restype = MagicNum.MsgTypec.REGISTERSUCCESSMSG
            self.addNewCPUser(_loginmsg[:-2] + _loginmsg[-1:])
            session.name = _loginmsg[0]
            from CryptoAlgorithms import RsaKeyExchange
            _rke = RsaKeyExchange.RsaKeyExchange()
            _rke.WritePubkeyStr(session.name, _loginmsg[-2])
            msgbody = _rke.GetPubkeyStr("own")
            msghead = self.packetMsg(restype,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody.decode('gbk').encode("utf-8") )
            