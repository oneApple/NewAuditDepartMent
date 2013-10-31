# -*- coding: UTF-8 -*-
class HashBySha1c:
    "二进制，十六进制"
    BINARY = 1001
    HEXADECIMAL = 1002
    
class ValidaDialogc:
    "头部显示图片还是静态文本"
    STATICTEXT = 2001
    IMAGEBUTTON = 2002

class NetAcceptc:
    "分别为最大监听数和绑定错误"
    MAXLISTENNUM = 3001
    BINDERROR = 3002
    
class CPUserTablec:
    "用户权限"
    UNACCEPT = 4001
    NORMAL = 4002    
    
class MediaTablec:
    "媒体状态"
    UNACCEPT = 5001
    ACCEPT = 5002
    AUDIT = 5003
    
class UserTypec:
    NOUSER = "nousertable"
    CPUSER = "cpusertable"

class NetConnectc:
    NOTCONNECT = 6001
        
class MsgTypec:
    "消息类型，三者之间必须相同"
    REQCLOSEMSG = 10001
    REQLOGINMSG = 10002
    REQREGISTERMSG = 10003
    REQAUDITMSG = 10004   
    
    LOGINSUCCESS = 11001
    LOGINFAIL = 11002  
    REGISTERSUCCESSMSG = 11003
    REGISTERFAIL = 11004 
    
    REQDHPANDPUBKEY = 11005
    SENDDHPANDPUBKEY = 11006  
    SENDDHPUBKEY = 11007
    AUDITDHGENERATE = 11008
    REQFILEBUFFER = 11009
    SENDFILEBUFFER = 11010
    SENDFILEOVER = 11011
    REQAGROUP = 11012
    SENDAGROUP = 11013
    RECVMEDIASUCCESS = 11014
    
    REQAUDITRETURN = 12001
    SENDFILENAME = 12002
    REQCGROUP = 12003
    SENDCGROUP = 12004
    AUDITRETURNDHGENERATE = 12005
    AUDITRETURNSUCCESS = 12006
    
    REQFILELIST = 20001
    REQOBTAINFILE = 20002
    SENDFILELIST = 20003
    OBTAINDHEGNERATE = 20004
    
    REQIDENTIFIED = 20005
    SENDSIGNELGAMAL1 = 20006
    SENDSIGNELGAMAL12 = 20007
    
    SENDHASHELGAMAL1 = 20008
    SENDHASHELGAMAL12 = 20009
    SENDIDENTIFYRES = 20010
    
    IDENTITYVERIFYFAILED = 13001