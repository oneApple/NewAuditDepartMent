# -*- coding: UTF-8 -*-
_metaclass_ = type
import os

from GlobalData import ConfigData, CommonData, MagicNum
from MsgHandle import MsgHandleInterface
from DataBase import MediaTable
from NetCommunication import NetSocketFun

class SendFileList(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendFileList,self).__init__()
    
    def getFileList(self):
        "获取文件列表"
        _filelist = []
        _cfg = ConfigData.ConfigData()
        _mediaPath = _cfg.GetMediaPath()
        if not os.path.exists(_mediaPath):
            os.mkdir(_mediaPath)
        _userDirList = os.listdir(_mediaPath)  
        
        for owner in _userDirList:
            _filenameList = os.listdir(_mediaPath + "/" + owner)
            for filename in _filenameList:
                _db = MediaTable.MediaTable()
                _db.Connect()
                _res = _db.searchMedia(filename, owner)
                _db.CloseCon()
                if _res == []:
                    break
                if _res[0][5] == MagicNum.MediaTablec.AUDIT:
                    _singleFile = [filename.encode("utf8"),owner.encode("utf8")]
                    _filelist.append(CommonData.MsgHandlec.PADDING.join(_singleFile))
            
        return _filelist
    
    def HandleMsg(self,bufsize,session):
        
        _fileList = self.getFileList()
        _msgbody =  CommonData.MsgHandlec.PADDING.join(_fileList)
        _msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILELIST, len(_msgbody))
        NetSocketFun.NetSocketSend(session.sockfd,_msghead + _msgbody)
        
        