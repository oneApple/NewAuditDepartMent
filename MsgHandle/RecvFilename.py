#coding=utf-8
_metaclass_ = type
from MsgHandle import MsgHandleInterface 
from GlobalData import ConfigData, MagicNum, CommonData
from NetCommunication import NetSocketFun

class RecvFilename(MsgHandleInterface.MsgHandleInterface,object):
    "接受文件名并打开文件准备写"
    def __init__(self):
        "获取接受文件路径"
        super(RecvFilename,self).__init__() 
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def createMediaDir(self,session):
        "创建目录"
        import os 
        self.___ownPath = self.__mediapath + "/" + session.peername
        if not os.path.exists(self.___ownPath):
            if not os.path.exists(self.__mediapath):
                os.mkdir(self.__mediapath)
            os.mkdir(self.___ownPath)
    
    def HandleMsg(self,bufsize,session):
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)[0]
        self.createMediaDir(session)
        session.filename = recvbuffer
        _localfilename = self.___ownPath + "/" + session.filename
        session.file = open(_localfilename.encode('utf-8'),"wb")
        session.currentbytes = 0
        NetSocketFun.NetSocketSend(session.sockfd,self.packetMsg(MagicNum.MsgTypec.REQDHPANDPUBKEY, 0))
        showmsg = "开始审核文件(" + recvbuffer + ")"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REFRESHSTATIC, [recvbuffer,"正在审核文件"])