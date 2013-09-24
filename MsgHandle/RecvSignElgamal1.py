# -*- coding: UTF-8 -*-

_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData, ConfigData
from CryptoAlgorithms import Elgamal, Rsa, HashBySha1
from DataBase import MediaTable
from NetCommunication import NetSocketFun

class RecvSignElgamal1(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvSignElgamal1,self).__init__() 
    
    def getAgroupSign(self,session,file,user):
        "获取文件A组采样签名"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.searchMedia(file,user)
        _db.CloseCon()
        _hbs = HashBySha1.HashBySha1()
        session.elgamallen = len(NetSocketFun.NetUnPackMsgBody(_res[0][4])) - 1
        return _hbs.GetHash(_res[0][3],MagicNum.HashBySha1c.HEXADECIMAL)
    
    def getCipherText(self,session):
        "将会话密钥加密"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        plaintext = session.sessionkey
        return _rsa.EncryptByPubkey(plaintext, session.peername)
    
    def packMsgBody(self,session):
        "消息内容：第一次加密类型，第一次加密结果，第二次加密类型，第二次加密结果"
        elgamal1 = session.elgamal.EncryptoList(Elgamal.StringToList(self.__asign))
        elgamal2 = session.elgamal.EncryptoList(self.__recvelgamal1)
        #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
        msglist = []
        msglist.append(self.getCipherText(session))
        msglist.append(Elgamal.GetStructFmt(elgamal1))
        msglist.append("".join(elgamal1))
        msglist.append(Elgamal.GetStructFmt(elgamal2))
        msglist.append("".join(elgamal2))
        #showmsg = "\n(2)第一次加密:" + repr(",".join(elgamal1)) + "\n(3)第二次加密结果:" +  repr(",".join(elgamal2))         
        #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
        return msglist
    
    def handRecvMsg(self,session,msgList):
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        _plaint = NetSocketFun.NetUnPackMsgBody(_rsa.DecryptByPrikey(eval(msgList[0])))
        if _plaint[0] == session.sessionkey:
            session.auditfile = msgList[1]
            session.audituser = msgList[2]
            self.__asign = self.getAgroupSign(session,msgList[1], msgList[2])
            import string
            session.elgamal = Elgamal.Elgamal(*[string.atol(s) for s in _plaint[1:]])
            import struct
            self.__recvelgamal1 = struct.unpack(msgList[3],eval(msgList[4]))
            showmsg = "A组签名的elgamal加密验证..."#：\n(1)接受到的第一次加密:" + repr(",".join(self.__recvelgamal1))            
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
            return True
        else:
            return False
    
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        msgList = NetSocketFun.NetUnPackMsgBody(recvmsg.encode("utf-8"))
        if self.handRecvMsg(session, msgList):
            msgbody = NetSocketFun.NetPackMsgBody(self.packMsgBody(session))
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDSIGNELGAMAL12,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
        else:
            showmsg = "会话密钥验证失败,发送方为恶意用户"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
