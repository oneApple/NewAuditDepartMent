# -*- coding: UTF-8 -*-
import wx,os

import ValidaDialog,RegisterDialog
from GlobalData import MagicNum, ConfigData
from DataBase import APUserTable

class LoginDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self):
        super(LoginDialog,self).__init__("登录",MagicNum.ValidaDialogc.IMAGEBUTTON)
        self.CheckConfig()
    
    def CheckConfig(self):
        try:
            cfg = ConfigData.ConfigData()
            pathmap = {cfg.GetDbPath():"数据库配置不正确",
               cfg.GetYVectorFilePath():"采样存放路径配置不正确",
               cfg.GetFfmpegPathAndArgs()[0]:"ffmpeg程序配置不正确",
               cfg.GetFfmpegPathAndArgs()[1]:"ffmpeg参数配置不正确",
               cfg.GetKeyPath():"密钥路径配置不正确",
               }
            for path in pathmap:
                if not os.path.exists(path):
                    self.setHeaderText(pathmap[path])
        except Exception,e:
            self.setHeaderText("配置文件不存在或路径错误")
            os.sys.exit()
            
    
    def getTextLabel(self):
        _labelList = ["用户名", "密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
                   审 核 部 门\
                """
        return _text
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        _db = APUserTable.APUserTable()
        _db.Connect()
        if not _db.VerifyNamePsw(_inputlist[0], _inputlist[1]):
            self.tryAgain("用户名或密码错误,请重新输入")
        else:
            self.SwitchView(_inputlist[0])
        _db.CloseCon()
    
    def registerButtonFun(self,event):
        self.Destroy()
        _dlg = RegisterDialog.RegisterDialog()
        _dlg.Run()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    dlg = LoginDialog()
    dlg.Run()
    app.MainLoop()
        
        

