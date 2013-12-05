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
    
    def getAgroupHash(self,auditfile,audituser):
        "获取文件A组特征提取签名"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.searchMedia(auditfile,audituser)
        _db.CloseCon()
        _hbs = HashBySha1.HashBySha1()
        return _res[0][4]
    
    def getCipherText(self,session):
        "对会话密钥进行加密"
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        plaintext = session.sessionkey
        return _rsa.EncryptByPubkey(plaintext, session.peername)
    
    def packMsgBody(self,session,msgList):
        hashlist = NetSocketFun.NetUnPackMsgBody(self.getAgroupHash(msgList[1], msgList[2]))
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REFRESHSTATIC, [msgList[1],"正在责任认定"])   

        session.auditfile = msgList[1]
        session.audituser = msgList[2]
        elgamallsit = []
        for cphash in hashlist:
            print cphash
            elgamal1 = session.elgamal.EncryptoList(Elgamal.StringToList(cphash))
            elgamallsit.append(Elgamal.GetStructFmt(elgamal1))
            elgamallsit.append("".join(elgamal1))
        showmsg = "一次加密Ａ组比特串承诺"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        return [self.getCipherText(session)] + elgamallsit
    
    def generateElgamal2(self,session,msgList):
        import struct
        session.elgamal2list = []
        for index in range(3,len(msgList),2):
            elgamal1 = struct.unpack(msgList[index],msgList[index + 1])
            elgamal2 = session.elgamal.EncryptoList(elgamal1)
            session.elgamal2list.append(Elgamal.GetStructFmt(elgamal2))
            session.elgamal2list.append("".join(elgamal2))
        showmsg = "二次加密Ａ组比特串承诺"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
    
    def handRecvMsg(self,session,msgList):
        _cfg = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfg.GetKeyPath())
        _plaint = NetSocketFun.NetUnPackMsgBody(_rsa.DecryptByPrikey(eval(msgList[0])))
        if _plaint[0] == session.sessionkey:
            import string
            session.elgamal = Elgamal.Elgamal(*[string.atol(s) for s in _plaint[1:]])
            return True
        else:
            return False
    
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        msgList = NetSocketFun.NetUnPackMsgBody(recvmsg)
        if self.handRecvMsg(session, msgList):
            msgbody = NetSocketFun.NetPackMsgBody(self.packMsgBody(session,msgList))
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDHASHELGAMAL1,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
            self.generateElgamal2(session, msgList)
        else:
            showmsg = "会话密钥验证失败,发送方为恶意用户"
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
            msghead = self.packetMsg(MagicNum.MsgTypec.IDENTITYVERIFYFAILED,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
