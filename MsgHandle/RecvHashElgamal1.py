# -*- coding: UTF-8 -*-

_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData, ConfigData
from CryptoAlgorithms import Elgamal, Rsa, HashBySha1
from DataBase import MediaTable
from NetCommunication import NetSocketFun

class RecvHashElgamal1(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvHashElgamal1,self).__init__() 
    
    def getAgroupHash(self,session):
        "获取文件A组采样签名"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.searchMedia(session.auditfile,session.audituser)
        _db.CloseCon()
        _hbs = HashBySha1.HashBySha1()
        return NetSocketFun.NetUnPackMsgBody(_res[0][4])[self.__index].encode("ascii")
    
    def getCipherText(self,session):
        "对会话密钥进行加密"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        plaintext = session.sessionkey
        return _rsa.EncryptByPubkey(plaintext, session.peername)
    
    def packMsgBody(self,session):
        elgamal1 = session.elgamal.EncryptoList(Elgamal.StringToList(self.__ahash))
        elgamal2 = session.elgamal.EncryptoList(self.__recvelgamal1)
        #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
        msglist = []
        msglist.append(self.getCipherText(session))
        msglist.append(str(self.__index)) 
        msglist.append(Elgamal.GetStructFmt(elgamal1))
        msglist.append("".join(elgamal1))
        msglist.append(Elgamal.GetStructFmt(elgamal2))
        msglist.append("".join(elgamal2))
        return msglist
    
    def handRecvMsg(self,session,msgList):
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        _plaint = NetSocketFun.NetUnPackMsgBody(_rsa.DecryptByPrikey(msgList[0]))
        if _plaint[0] == session.sessionkey:
            import struct, string
            self.__index = string.atoi(msgList[1])
            self.__ahash = self.getAgroupHash(session)
            #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
            session.elgamal = Elgamal.Elgamal(*[string.atol(s) for s in _plaint[1:]])
            self.__recvelgamal1 = struct.unpack(msgList[2],msgList[3])
            showmsg = "进行第一次加密，第一次加密结果发送给NO\n"
            showmsg += "进行第二次加密，第二次加密结果发送给NO"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
            showmsg = "A组采样的elgamal加密第 " + msgList[1] + " 组并进行验证"# + ",".join(self.__recvelgamal1)
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
            if self.__index == session.elgamallen:
                showmsg = "加密验证结束"
                self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
            return True
        else:
            return False
    
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        msgList = NetSocketFun.NetUnPackMsgBody(recvmsg)
        if self.handRecvMsg(session, msgList):
            msgbody = NetSocketFun.NetPackMsgBody(self.packMsgBody(session))
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDHASHELGAMAL12,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
        else:
            showmsg = "会话密钥验证失败,发送方为恶意用户"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
