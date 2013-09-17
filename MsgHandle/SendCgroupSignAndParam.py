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
        showmsg = "C组采样过程："
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        _cgvs = GetVideoSampling.GetVideoSampling(_filename,*_cparam)
        return [str(x) for x in _cparam],  CommonData.MsgHandlec.PADDING.join(_cgvs.GetSampling())
    
    def packMsgBody(self,session):
        _cgroup = self.getCgroupHashAndParam(session)
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        _plaintext = str(session.sessionkey) + CommonData.MsgHandlec.PADDING + CommonData.MsgHandlec.PADDING.join(_cgroup[0])
        _pubkeyMsg = _rsa.EncryptByPubkey(_plaintext.encode("ascii"), session.peername)
        
        _hbs = HashBySha1.HashBySha1()
        _sign = _rsa.SignByPrikey(_hbs.GetHash(_cgroup[1].encode("ascii"),MagicNum.HashBySha1c.HEXADECIMAL))
        _msgbody = _pubkeyMsg + CommonData.MsgHandlec.PADDING + _sign + CommonData.MsgHandlec.PADDING + _cgroup[1].encode("ascii")
        showmsg = "发送采样结果：\n(1)C组参数：" + ",".join(_cgroup[0]) + "\n(2)C组采样:" + _cgroup[1] + "\n(3)C组采样签名：" + _sign 
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
        