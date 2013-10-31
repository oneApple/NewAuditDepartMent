# -*- coding: UTF-8 -*-
import wx

import ValidaDialog
from GlobalData import MagicNum
from DataBase import APUserTable


class RegisterDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self):
        super(RegisterDialog,self).__init__("注册",MagicNum.ValidaDialogc.STATICTEXT)
    
    def getTextLabel(self):
        _labelList = ["用户名","密码","重复密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
                \n 欢 迎 注 册 系 统
                """
        return _text
    
    def addNewUser(self,inputlist):
        
        _db = APUserTable.APUserTable()
        _db.Connect()
        if not _db.AddNewUser(inputlist[0], inputlist[1]):
            self.tryAgain("用户已存在")
            _db.CloseCon()
            return
        _db.CloseCon()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        if _inputlist[1] != _inputlist[2]:
            self.tryAgain("密码输入不一致")
        else:
            self.addNewUser(_inputlist)
            self.SwitchView(_inputlist[0])
            
        
if __name__=='__main__':
    app = wx.PySimpleApp()
    dlg = RegisterDialog()
    dlg.Run()
    app.MainLoop()