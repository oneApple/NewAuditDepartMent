# -*- coding: UTF-8 -*-

_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from NetCommunication import NetSocketFun
from DataBase import MediaTable

class RecvIdentifyRes(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvIdentifyRes,self).__init__() 
        self.responmsg = {CommonData.Response.AP:"网络运营商和内容提供商无过错",
                          CommonData.Response.CP:"审核部门和运营商保存的内容提供商签名不同，所以内容提供商篡改文件",
                          CommonData.Response.NO:"文件特征提取验证失败，所以运营商篡改文件"}
    
    def getAgroupParam(self,session):
        "获取文件A组特征提取签名"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.searchMedia(session.auditfile,session.audituser)
        _db.CloseCon()
        
        print _res[0][2]
        
        return NetSocketFun.NetUnPackMsgBody(_res[0][2])
    
    def showresult(self,session,difList):
        import string
        aparam = self.getAgroupParam(session)
        _fnum = string.atoi(aparam[0])
        _gt = string.atoi(aparam[1])
        
        _groupborder = [x * (_fnum / _gt) for x in range(_gt)] + [_fnum]
        
        if len(difList) == 0:
            showmsg = "结果：特征提取验证成功，该文件未被篡改"
        else:
            showmsg = "结果：特征提取验证失败，该文件被篡改,其中"
        for _dif in difList:
            showmsg += "\n第" + str(_dif) + "组存在篡改，篡改帧区间为：" + str(_groupborder[_dif]) + "-" + str(_groupborder[_dif + 1]) +"帧"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
    
    def HandleMsg(self,bufsize,session):
        "接收所有文件"
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        recvbuffer = NetSocketFun.NetUnPackMsgBody(recvmsg)
        
        import string
        showmsg = self.responmsg[string.atoi(recvbuffer[0])]
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        
        self.showresult(session, [string.atoi(index) for index in recvbuffer[1:]])

