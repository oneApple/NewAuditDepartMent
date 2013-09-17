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
        return _res[0][4].split(CommonData.MsgHandlec.PADDING)[self.__index].encode("ascii")
    
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
        _cipher = self.getCipherText(session)
        _plaintext = str(self.__index) + CommonData.MsgHandlec.PADDING + Elgamal.GetStructFmt(elgamal1) + CommonData.MsgHandlec.PADDING + \
                     "".join(elgamal1) + CommonData.MsgHandlec.PADDING + \
                     Elgamal.GetStructFmt(elgamal2) + CommonData.MsgHandlec.PADDING + \
                     "".join(elgamal2)
        #showmsg = "\n(3)第一次加密结果:" + ",".join(elgamal1) + "\n(4)第二次加密结果:" + ",".join(elgamal2)
        #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
        return _cipher + CommonData.MsgHandlec.PADDING + _plaintext
    
    def handRecvMsg(self,session,msgList):
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        _plaint = _rsa.DecryptByPrikey(msgList[0]).split(CommonData.MsgHandlec.PADDING)
        if _plaint[0] == session.sessionkey:
            import struct, string
            self.__index = string.atoi(msgList[1])
            self.__ahash = self.getAgroupHash(session)
            #self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
            session.elgamal = Elgamal.Elgamal(*[string.atol(s) for s in _plaint[1:]])
            self.__recvelgamal1 = struct.unpack(msgList[2],msgList[3])
            showmsg = "A组采样的elgamal加密第 " + msgList[1] + " 组并进行验证"# + ",".join(self.__recvelgamal1)
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
            if self.__index == session.elgamallen:
                showmsg = "加密验证结束"
                self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
            return True
        else:
            return False
    
    def HandleMsg(self,bufsize,session):
        recvbuffer = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        msgList = recvbuffer.split(CommonData.MsgHandlec.PADDING)
        if self.handRecvMsg(session, msgList):
            msgbody = self.packMsgBody(session)
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDHASHELGAMAL12,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
        else:
            showmsg = "会话密钥验证失败,发送方为恶意用户"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
