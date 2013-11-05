# -*- coding: UTF-8 -*-
_metaclass_ = type

from GlobalData.MagicNum import MsgTypec 
import SendLoginResult, SendRegisterResult, RecvAndSendDh, IdentifyVerifyFailed, RecvAuditDhGenerate, \
       RecvFilename, RecvFileBuffer, RecvAllFile, RecvAgroupSignAndParam, SendDhPAndPubkey,\
       SendFileBuffer, SendCgroupSignAndParam, RecvAuditReturnSuccess, RecvDhPubkeyAndSendDhGenerateSuccess,\
       RecvHashElgamal1, RecvHashElgamal2, SendFileList,RecvIdentifyRes
       

class MsgHandleMap:
    def __init__(self):
        "消息类型与处理类之间的关系"
        self.__MsgHandleMap = {MsgTypec.REQLOGINMSG:SendLoginResult.SendLoginResult(),
                               #返回登录结果
                               MsgTypec.REQREGISTERMSG:SendRegisterResult.SendRegisterResult(),
                               #返回注册结果
                               MsgTypec.REQCLOSEMSG:IdentifyVerifyFailed.IdentifyVerifyFailed(),
                               MsgTypec.REQAUDITMSG:RecvFilename.RecvFilename(),                              
                               MsgTypec.SENDDHPANDPUBKEY:RecvAndSendDh.RecvAndSendDh(),
                               
                               MsgTypec.IDENTITYVERIFYFAILED:IdentifyVerifyFailed.IdentifyVerifyFailed(),
                               
                               MsgTypec.REQAUDITMSG:RecvFilename.RecvFilename(),
                               MsgTypec.AUDITDHGENERATE:RecvAuditDhGenerate.RecvAuditDhGenerate(),
                               MsgTypec.SENDFILEBUFFER:RecvFileBuffer.RecvFileBuffer(),
                               MsgTypec.SENDFILEOVER:RecvAllFile.RecvAllFile(),
                               MsgTypec.SENDAGROUP:RecvAgroupSignAndParam.RecvAgroupSignAndParam(),
                               
                               MsgTypec.AUDITRETURNDHGENERATE:SendFileBuffer.SendFileBuffer(),
                               MsgTypec.REQFILEBUFFER:SendFileBuffer.SendFileBuffer(),
                               MsgTypec.REQCGROUP:SendCgroupSignAndParam.SendCgroupSignAndParam(),
                               MsgTypec.AUDITRETURNSUCCESS:RecvAuditReturnSuccess.RecvAuditReturnSuccess(),
                               
                               MsgTypec.REQIDENTIFIED:SendDhPAndPubkey.SendDhPAndPubkey(),
                               MsgTypec.SENDDHPUBKEY:RecvDhPubkeyAndSendDhGenerateSuccess.RecvDhPubkeyAndSendDhGenerateSuccess(),
                               MsgTypec.SENDHASHELGAMAL1:RecvHashElgamal1.RecvHashElgamal1(),
                               MsgTypec.SENDHASHELGAMAL2:RecvHashElgamal2.RecvHashElgamal2(),
                               
                               MsgTypec.REQFILELIST:SendFileList.SendFileList()
                               }      
                             
    def getMsgHandle(self,msgtype):
        "通过消息类型返回具体的处理类"
        assert(self.__MsgHandleMap.has_key(msgtype))
        return self.__MsgHandleMap[msgtype]