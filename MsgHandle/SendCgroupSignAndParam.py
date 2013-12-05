#coding=utf-8
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData
from VideoSampling import GetVideoSampling
from CryptoAlgorithms import Rsa, HashBySha1
from NetCommunication import NetSocketFun

class SendCgroupSignAndParam(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendCgroupSignAndParam,self).__init__()
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def getCgroupHashAndParam(self,session):
        _dir = session.filename
        _filename   = _dir[-_dir[::-1].index("/"):-_dir[::-1].index(".") - 1]
        #_gsp = GetSamplingParams.GetSamplingParams(_filename)
        _cparam = session.control.cparams#_gsp.GetSamplingParams()
        
#        _meidaPath = self.__mediapath + "/" + session.peername + "/" + _dir[-_dir[::-1].index("/"):]
#        _efm = ExecuteFfmpeg.ExecuteFfmpeg(_meidaPath)
#        _efm.Run()
#        _efm.WaitForProcess()
        showmsg = "C组特征提取过程："
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        _cgvs = GetVideoSampling.GetVideoSampling(_filename,*_cparam)
        return [str(x) for x in _cparam] , NetSocketFun.NetPackMsgBody(_cgvs.GetSampling())
    
    def packMsgBody(self,session):
        _cgroup = self.getCgroupHashAndParam(session)
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        msglist = [str(session.sessionkey)] + _cgroup[0]
        _plaintext = NetSocketFun.NetPackMsgBody(msglist)
        _pubkeyMsg = _rsa.EncryptByPubkey(_plaintext.encode("ascii"), session.peername)
        
        _hbs = HashBySha1.HashBySha1()
        _sign = _rsa.SignByPrikey(_hbs.GetHash(_cgroup[1].encode("ascii"),MagicNum.HashBySha1c.HEXADECIMAL))
        msglist = [_pubkeyMsg,_sign,_cgroup[1].encode("ascii")]
        _msgbody = NetSocketFun.NetPackMsgBody(msglist)
        showmsg = "发送特征提取结果：\n(1)C组参数：" + ",".join(_cgroup[0]) + "\n(2)C组特征提取:" + \
                  CommonData.MsgHandlec.SHOWPADDING.join(NetSocketFun.NetUnPackMsgBody(_cgroup[1])) + "\n(3)C组特征提取签名：" + _sign 
        showmsg += "\n等待文件验证..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        return _msgbody
    
    def deltempFile(self,filename):
        import os
        _cfg = ConfigData.ConfigData()
        _mediapath = _cfg.GetYVectorFilePath()
        _media = _mediapath + "out.ts" 
        try:
            os.remove(_media)
        except:
            pass
        _dir = _mediapath + filename[:filename.index(".")]
        for root, dirs, files in os.walk(_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)  
    
    def HandleMsg(self,bufsize,session):
        msgbody = self.packMsgBody(session)
        msghead = self.packetMsg(MagicNum.MsgTypec.SENDCGROUP,len(msgbody))
        NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
        
        _dir = session.filename
        _filename   = _dir[-_dir[::-1].index("/"):]
        self.deltempFile(_filename)
        
if __name__ == "__main__":
    pass    
        