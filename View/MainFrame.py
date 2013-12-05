# -*- coding: UTF-8 -*-
import wx, os
from wx.lib.pubsub  import Publisher

from NetCommunication import NetAccept
from GlobalData import CommonData, MagicNum, ConfigData, WindowConfig
from DataBase import MediaTable
import MatrixTable ,FullScreenFrame


class MyFrame(wx.Frame):
    def __init__(self,username):
        self.wcfg = WindowConfig.WindowConfig()
        wx.Frame.__init__(self, None, -1, "内容保护子系统-互信系统",size = self.wcfg.GetFrameSize())
        
        self.__vbox_top = wx.BoxSizer(wx.VERTICAL)
        self.__hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.__panel_top = wx.Panel(self)
        
        self.createHeadStaticText(text = "您好:" + username + ",欢迎使用内容保护子系统-互信系统!"+ "\n")
        self.createHeadStaticText(align = wx.ALIGN_LEFT,text ="\n" + " 审核部门" + "\n",\
                                  fontsize = self.wcfg.GetSystemNameFontSize(),\
                                  fontcolor = self.wcfg.GetSystemNameFontColor(),\
                                  backcolor = self.wcfg.GetSystemNameBackColor())
        self.__vbox_top.Add(wx.StaticLine(self.__panel_top), 0, wx.EXPAND|wx.ALL, 5)
        self.createMenuBar()
        
        self.createLeft()
        self.createShowTextCtrl()
        
        self.__vbox_top.Add(self.__hbox,proportion=2,flag = wx.EXPAND)
        self.__vbox_top.Add(wx.StaticLine(self.__panel_top), 0, wx.EXPAND|wx.ALL, 5)
        self.createHeadStaticText(text = "CopyRight@CUC 2013")
        #self.__vbox_top.Add(wx.StaticLine(self.__panel_top), 0, wx.EXPAND|wx.ALL, 5)
        self.__panel_top.SetSizer(self.__vbox_top)
        self.registerPublisher()
        
        #记录列表选择的位置
        self.__gridCurPos = -1
        self.__showTextColor = True
        self.username = username
        
        from CryptoAlgorithms import RsaKeyExchange
        _rke = RsaKeyExchange.RsaKeyExchange()
        _rke.GenerateRsaKey()
        
        self.fullframe = FullScreenFrame.FullScreenFrame(self,-1,"信息显示区")    
        
        _netaccept = NetAccept.NetAccept(self)
        _netaccept.startNetConnect()
    
    def registerPublisher(self):
        Publisher().subscribe(self.rewriteShowTextCtrl, CommonData.ViewPublisherc.MAINFRAME_REWRITETEXT)    
        Publisher().subscribe(self.appendShowTextCtrl, CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT)    
        Publisher().subscribe(self.refreshStaticText, CommonData.ViewPublisherc.MAINFRAME_REFRESHSTATIC)
        Publisher().subscribe(self.refreshFileList, CommonData.ViewPublisherc.MAINFRAME_REFRESHFILETABLE)
    
    def rewriteShowTextCtrl(self,recvmsg):
        "删除最后一行，并添加新行"
        msg = recvmsg.data[0].decode("utf8")
        
        _text = self.__showText.GetValue()
        self.__showText.Clear()
        _textlist = _text.split("\n")
        _textlist = _textlist[:-2] + [msg,]
        
        _isChangeColor = recvmsg.data[1]
        if _isChangeColor:
            if self.__showTextColor:
                self.__showText.SetForegroundColour(self.wcfg.GetShowTextFontColor1())
            else:
                self.__showText.SetForegroundColour(self.wcfg.GetShowTextFontColor2())
                
        self.__showText.SetValue("\n".join(_textlist) + "\n")
    
    def appendShowTextCtrl(self,recvmsg):
        "添加新行"
        msg = recvmsg.data[0].decode("utf8")
        msg += "\n"
        
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.FULLFRAME_APPENDTEXT,recvmsg.data)
        
        _isChangeColor = recvmsg.data[1]
        if _isChangeColor:
            if self.__showTextColor:
                self.__showText.SetForegroundColour(self.wcfg.GetShowTextFontColor1())
            else:
                self.__showText.SetForegroundColour(self.wcfg.GetShowTextFontColor2())
            self.__showTextColor = not self.__showTextColor
        self.__showText.AppendText(msg)
    
    def evtShowTextDoubleClick(self,evt):
        self.fullframe.ShowFullScreenFrame()
        self.Hide()
    
    def createShowTextCtrl(self):
        "创建右下方的文本显示框"
        _panel = self.createPanel(self.__panel_top)
        
        self.__showText = wx.TextCtrl(_panel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)  
        self.__showText.SetFont(self.wcfg.GetShowTextFont())
        self.__showText.SetBackgroundColour(self.wcfg.GetShowTextBackColor())
        self.__showText.Bind(wx.EVT_LEFT_DCLICK, self.evtShowTextDoubleClick)
        
        self.createBox([self.__showText, ], _panel, self.__hbox, "信息显示区", 3)
    
    def createPanel(self,outpanel,color = "mistyrose"):
        _panel = wx.Panel(outpanel,-1)
        _panel.SetBackgroundColour(color)
        return _panel
    
    def createBox(self,componentlist,innerpanel,outbox,label,partition = 1,align = wx.EXPAND):
        box = wx.StaticBox(innerpanel,-1,label)
        vbox = wx.StaticBoxSizer(box,wx.HORIZONTAL)
        
        for component in componentlist:
            vbox.Add(component,1,align)
        
        innerpanel.SetSizer(vbox)
        outbox.Add(innerpanel,partition,align)
        return vbox
    
    def createLeft1Static(self,panel,hbox):
        ""
        _panel = self.createPanel(panel)
        
        stext = wx.StaticText(_panel, -1, "")
        Font = self.wcfg.GetStaticTextFont()
        stext.SetFont(Font)
        stext.SetForegroundColour(self.wcfg.GetStaticTextFontColor())

        self.createBox([stext,], _panel, hbox, "操作结果区")
        
        return stext
    
    def getFrameNum(self):
        "获取目录下文件数即帧的数目"
        if self.__gridCurPos == -1:
            return
        
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        _cfg = ConfigData.ConfigData()
        _mediadir = _cfg.GetYVectorFilePath() + _filename[:_filename.find(".")]
        self.__framenum = sum([len(files) for root,dirs,files in os.walk(_mediadir)])
        for _sc in [self.__groupSpin,self.__gapSpin]:
            _sc.SetRange(1,self.__framenum)
            _sc.SetValue(1) 
    
    def evtGridRowLabelLeftClick(self,evt):
        "左键单击行标签"
        _pos = evt.GetRow()
        
        if _pos == -1 or _pos == self.__gridCurPos:
            return
        
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(self.wcfg.GetTableChoseFontColor())
        attr.SetBackgroundColour(self.wcfg.GetTableChoseBackColor())
        self.__grid.SetRowAttr(_pos, attr)
        
        if self.__gridCurPos != -1:
            attr = wx.grid.GridCellAttr()
            self.__grid.SetRowAttr(self.__gridCurPos, attr)
        
        #_filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        #self.refreshStaticText([_filename,"选择"])
        
        self.__gridCurPos = _pos
        self.__grid.Hide()
        self.__grid.Show()
        self.getFrameNum()
    
    def evtBtnAuditClick(self,evt):
        "审核按钮触发事件"
        if self.__gridCurPos == -1:
            return
        
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        self.refreshStaticText([_filename,"审核"])
        
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        _ownername = self.__grid.GetCellValue(self.__gridCurPos,1)
        _cfg = ConfigData.ConfigData()
        _path = _cfg.GetMediaPath() + "/" + _ownername + "/" + _filename
        from VlcMedia import MediaPlayer
        _mp = MediaPlayer.MediaPlayer()
        _mp.Plyaer(_path)
    
    def evtBtnSamplingClick(self,evt):
        "触发特征提取"
        if self.__gridCurPos == -1:
            return
        
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        _ownername = self.__grid.GetCellValue(self.__gridCurPos,1)
        _cfg = ConfigData.ConfigData()
        _path = _cfg.GetMediaPath() + "/" + _ownername + "/" + _filename
        
        self.refreshStaticText([_filename,"预提取"])
        
        from ProcessDialog import ProcessDialog
        frame = ProcessDialog(_path,self)
        frame.Run()
            
    def evtBtnDelClick(self,evt):
        "删除按钮触发事件"
        if self.__gridCurPos == -1:
            return
        
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        _ownername = self.__grid.GetCellValue(self.__gridCurPos,1)
        _cfg = ConfigData.ConfigData()
        _path = _cfg.GetMediaPath() + "/" + _ownername + "/" + _filename
        
        _db = MediaTable.MediaTable()
        _db.Connect()
        _db.deleteMedia(_filename,_ownername)
        _db.CloseCon()
        
        try:
            os.remove(_path)
            if os.listdir(_cfg.GetMediaPath() + "/" + _ownername) == []:
                os.rmdir(_cfg.GetMediaPath() + "/" + _ownername)
        except:
            pass
        
        self.__gridCurPos = -1
        self.refreshStaticText([_filename,"删除"])
        self.refreshFileList()
    
    def getSamplingParams(self):
        def handleSamplingParams(params):
            import string
            return list(params[:3]) + [string.atof(str(s)) for s in params[3:]]
        import random
        _valueList = []
        for _value in [self.__groupSpin,self.__gapSpin]:
            _valueList.append(_value.GetValue())
        cparams = [self.__framenum,_valueList[0],_valueList[1],random.random(),random.uniform(3.5699456,4.0)]
        return handleSamplingParams(cparams)
    
    def evtBtnAuditRetrunClick(self,evt):
        "审核返回事件"
        def getIpAndPort(username):
            _cfg = ConfigData.ConfigData();
            addrlist = _cfg.GetContentServerAddress()
            namelist = addrlist[0].split(",")
            iplist = addrlist[1].split(",")
            portlist = addrlist[2].split(",")
            for index in range(len(namelist)):
                if namelist[index] == username:
                    return iplist[index],portlist[index]
        
        if self.__gridCurPos == -1:
            return
        _filename = self.__grid.GetCellValue(self.__gridCurPos,0)
        _ownername = self.__grid.GetCellValue(self.__gridCurPos,1)
        _cfg = ConfigData.ConfigData()
        _path = _cfg.GetMediaPath() + "/" + _ownername + "/" + _filename
        
        self.refreshStaticText([_filename,"正在审核返回"])        
        from NetCommunication import NetConnect
        self.netConnect = NetConnect.NetConnect(self)
        if self.netConnect.StartNetConnect(*getIpAndPort(_ownername)) == MagicNum.NetConnectc.NOTCONNECT:
            wx.MessageBox("无法连接该内容提供商","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
            return
        
        import time
        time.sleep( 2 )
        self.netConnect.ReqAuditReturn(_path,self.getSamplingParams())
        
        #将媒体状态改为通过审核
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.AlterMedia("status", MagicNum.MediaTablec.AUDIT, _filename, _ownername)
        _db.CloseCon()
    
    def refreshStaticText(self,recvmsg):
        "刷新信息显示区"
        _recvmsg = recvmsg
        if type(recvmsg) != list:
            _recvmsg = recvmsg.data
        showmsg = "处理文件:"+ _recvmsg[0] + "\n"
        showmsg += "当前状态:" + _recvmsg[1]
        self.__infoStatic.SetLabel(showmsg)
    
    def refreshFileList(self,recvmsg = ""):
        "更新文件列表"
        _filelist = self.getFileList()
        _m = MatrixTable.MatrixTable(_filelist,["文件名","所有者","状态"],[i for i in range(len(_filelist))])
        self.__grid.ClearGrid()#清空表格
        self.__grid.SetTable(_m)
        self.__grid.Hide()
        self.__grid.Show()
    
    def getFileList(self):
        "获取文件列表"
        _filelist = []
        _cfg = ConfigData.ConfigData()
        _mediaPath = _cfg.GetMediaPath()
        if not os.path.exists(_mediaPath):
            os.mkdir(_mediaPath)
        
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.Search("select * from MediaTable")
        _db.CloseCon()
        
        for index in range(len(_res)):
            status = "未审核"
            if _res == []:
                return []
            if _res[index][5] == MagicNum.MediaTablec.AUDIT:
                status = "已审核"
            _singleFile = [_res[index][0], _res[index][1], status]
            _filelist.append(_singleFile)
            
        return _filelist
    
    def createLeft2FileTable(self,panel,vbox):
        "文件列表"
        _panel = self.createPanel(panel)
        self.__grid = wx.grid.Grid(_panel)
        table = MatrixTable.MatrixTable(self.getFileList(),["文件名","所有者","状态"],[i for i in range(3)])
        self.__grid.SetTable(table, True)
        self.__grid.SetRowLabelSize(self.wcfg.GetTableLabelSize())
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.evtGridRowLabelLeftClick)
        
        self.createBox([self.__grid,], _panel, vbox, "文件操作区",partition = 2)
        
    def createLeft3Button(self,panel,vbox):
        _panel = self.createPanel(panel)
        
        _Button1 = wx.Button(_panel,-1,"审核")
        self.Bind(wx.EVT_BUTTON,self.evtBtnAuditClick ,_Button1)
        _Button2 = wx.Button(_panel,-1,"预提取")
        self.Bind(wx.EVT_BUTTON,self.evtBtnSamplingClick ,_Button2)
        _Button3 = wx.Button(_panel,-1,"删除")
        self.Bind(wx.EVT_BUTTON,self.evtBtnDelClick ,_Button3)
        
        self.createBox([_Button1,_Button2,_Button3], _panel, vbox, "",partition = 0.5,align = wx.ALIGN_RIGHT)
    
    def OnScrollChanged(self,event):
        "spin改变触发事件"
        if self.__gridCurPos == -1:
            return
        def getGroupLen(framenum,gt,glen):
            "获取分组长度(参数X),_glen是每组的帧数目"
            _glen = glen - 1
            _x = 1
            while _glen >= 2:
                _glen = _glen / 2
                _x += 1
                if (framenum / gt - 1) < 2 ** _x:
                    _x -= 1
            return _x
        
        _spin = event.GetEventObject()
        if _spin == self.__groupSpin:
            _value = getGroupLen(self.__framenum,_spin.GetValue(), self.__framenum / _spin.GetValue())
            self.__gapSpin.SetRange(1,_value)
            self.__gapSpin.SetValue(1)
         
    def createLeft4Spin(self,panel,vbox,spinlabel = "",boxlabel = ""):
        "参数选择"
        _panel = self.createPanel(panel)
        _label = wx.StaticText(_panel,-1,spinlabel)
        _sc = wx.SpinCtrl(_panel, -1,size = (100,30))
        _sc.SetRange(1,1)
        _sc.SetValue(1) 
        self.Bind(wx.EVT_SPINCTRL, self.OnScrollChanged,_sc)
        self.createBox([_label,_sc], _panel, vbox, boxlabel,partition = 0.5)
        return _sc
    
    def createLeft5Button(self,panel,vbox):
        "审核返回按钮"
        _panel = self.createPanel(panel)
        
        _Button1 = wx.Button(_panel,-1,"审核返回")
        self.Bind(wx.EVT_BUTTON,self.evtBtnAuditRetrunClick,_Button1)
        
        self.createBox([_Button1], _panel, vbox, "",partition = 0.5,align = wx.ALIGN_RIGHT)    
        
    def createLeft(self):
        "创建左下方的文本显示框"
        panel = self.createPanel(self.__panel_top)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.__infoStatic = self.createLeft1Static(panel,vbox)
        
        vbox.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 20)
        
        self.createLeft2FileTable(panel,vbox)
        self.createLeft3Button(panel, vbox)
        
        vbox.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.ALL, 20)
        
        self.__groupSpin = self.createLeft4Spin(panel, vbox,spinlabel = "C 组 组 数",boxlabel = "参数选择区")
        self.__gapSpin = self.createLeft4Spin(panel, vbox,spinlabel = "C组帧间隔")
        
        self.createLeft5Button(panel, vbox)
        
        panel.SetSizer(vbox)
        self.__hbox.Add(panel,1,wx.EXPAND)
        #地一个参数是部件，第二个参数是所占比例，1是100,2是50,第三个是排列方式

    def createHeadStaticText(self,align = wx.ALIGN_CENTER,fontsize = 10,text = "",fontcolor = "black",backcolor = "white"):
        "创建位于上方的静态显示框"
        panel = self.createPanel(self.__panel_top,backcolor)
        
        stext = wx.StaticText(panel, -1, text)
        Font= wx.Font(fontsize, wx.MODERN, wx.NORMAL, wx.NORMAL)
        stext.SetFont(Font)
        stext.SetForegroundColour(fontcolor)
        stext.SetBackgroundColour(backcolor)
        
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(stext,0,align)
        panel.SetSizer(hbox)
        self.__vbox_top.Add(panel,0,wx.EXPAND)
        
    def createMenuBar(self):
        self.__menuBar = wx.MenuBar()
        for _label in CommonData.MainFramec.menuMap:
            self.createMenu(self.__menuBar, _label, CommonData.MainFramec.menuMap[_label])
        self.SetMenuBar(self.__menuBar)
    
    def createMenu(self,parentMenu,label,child):
        if type(child) == dict:
            menu = wx.Menu()
            if parentMenu == self.__menuBar: 
                parentMenu.Append(menu, label)
            else:
                parentMenu.AppendMenu(-1, label, menu)
            for _label in child:
                self.createMenu(menu, _label, child[_label])
        else:
            menuitem = parentMenu.Append(-1,label)
            self.Bind(wx.EVT_MENU, getattr(self,"menu" + child + "Cmd"), menuitem)
        
    def menuCPUserAuditCmd(self, event):
        import AlterCPUserPermissionsDialog
        _dlg = AlterCPUserPermissionsDialog.AlterCPUserPermissionDialog("选择用户",MagicNum.CPUserTablec.UNACCEPT)
        _dlg.Run()
    
    def menuDeleteCPUserCmd(self,event):
        import DeleteCPUserDialog
        _dlg = DeleteCPUserDialog.DeleteCPUserDialog("删除用户")
        _dlg.Run()
    
    def menuNOUserAuditCmd(self, event):
        import AlterNOUserPermissionsDialog
        _dlg = AlterNOUserPermissionsDialog.AlterNOUserPermissionDialog("选择用户",MagicNum.CPUserTablec.UNACCEPT)
        _dlg.Run()
    
    def menuDeleteNOUserCmd(self,event):
        import DeleteNOUserDialog
        _dlg = DeleteNOUserDialog.DeleteNOUserDialog("删除用户")
        _dlg.Run()
    
    def menuAPUserAuditCmd(self, event):
        import AlterAPUserPermissionsDialog
        _dlg = AlterAPUserPermissionsDialog.AlterAPUserPermissionDialog("选择用户",MagicNum.CPUserTablec.UNACCEPT)
        _dlg.Run()
    
    def menuDeleteAPUserCmd(self,event):
        import DeleteAPUserDialog
        _dlg = DeleteAPUserDialog.DeleteAPUserDialog("删除用户")
        _dlg.Run()
    
    def menuClearDisplayCmd(self,event):
        self.__showText.Clear()
        self.fullframe.clearShowText()
    
    def Run(self):
        self.Center()
        self.Show()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame("root")
    frame.Run()
    app.MainLoop()