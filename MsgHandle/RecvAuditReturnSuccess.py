# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from DataBase import MediaTable
from GlobalData import MagicNum, CommonData
from NetCommunication import NetSocketFun
import struct

class RecvAuditReturnSuccess(MsgHandleInterface.MsgHandleInterface,object):
    "身份验证成功"
    def __init__(self):
        super(RecvAuditReturnSuccess,self).__init__() 
        
    def getFilename(self,session):
        _filename = session.filename[-session.filename[::-1].index("/"):]
        return _filename
    
    def HandleMsg(self,bufsize,session):
        _db = MediaTable.MediaTable()
        _db.Connect()
        _medianame = self.getFilename(session)
        _db.AlterMedia("status", MagicNum.MediaTablec.AUDIT, _medianame, session.peername)
        _db.CloseCon()
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REFRESHFILETABLE, "")
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, "内容端接收("+ _medianame +")及参数成功",True)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_REFRESHSTATIC, [_medianame,"审核返回完毕"])
        _msghead = self.packetMsg(MagicNum.MsgTypec.REQCLOSEMSG, 0)
        NetSocketFun.NetSocketSend(session.sockfd,_msghead)
        session.stop()
        
        
        
