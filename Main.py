from View import LoginDialog
import wx, sys

reload(sys)                         
sys.setdefaultencoding('utf-8')  

app = wx.PySimpleApp()
dlg = LoginDialog.LoginDialog()
dlg.Run()
app.MainLoop()