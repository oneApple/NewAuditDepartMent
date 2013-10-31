# -*- coding: UTF-8 -*-
class MsgHandlec:
    MSGHEADTYPE = 'ii'
    SAMPLINGTYPE = "fffff"
    PADDING = "###"
    SHOWPADDING = "::"
    ELGAMALPAD = "#####"
    FILEBLOCKSIZE = 10240

class ViewPublisherc:
    MAINFRAME_REWRITETEXT = "mainframerewritetext"
    MAINFRAME_APPENDTEXT = "mainframeappendtext"
    MAINFRAME_REFRESHSTATIC = "mainframerefstatic"
    MAINFRAME_REFRESHFILETABLE = "mainframereffiletable"
    FULLFRAME_APPENDTEXT = "fullframeappendtext"

class MainFramec:
    "菜单"
    cpusermenu = {"用户审核":"CPUserAudit","用户删除":"DeleteCPUser"}
    nousermenu = {"用户审核":"NOUserAudit","用户删除":"DeleteNOUser"}
    apusermenu = {"用户删除":"DeleteAPUser"}
    usermenu = {"审核部门用户管理":apusermenu,"内容提供商用户管理":cpusermenu,"网络运营商用户管理":nousermenu}
    toolmenu = {"清理屏幕".decode("utf8"):"ClearDisplay"}
    menuMap = {"用户管理":usermenu,"工具":toolmenu}
    disablemenu = ["用户审核","用户删除"]

class Rsac:
    "密钥及明文长度:对应关系为:1024:128,2048:256"
    KEYLEN = 1024
    PLAINTLEN = 128    
    
class HashBySha1c:
    "哈希后的长度"
    BINARYHASH = 20
    HEXHASH = 40

class SamplingFrameArrayc:
    GROUPPARAMELEN = 7

class Response:
    AP = 0
    CP = 1
    NO = 2