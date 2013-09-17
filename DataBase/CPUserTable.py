# -*- coding: UTF-8 -*-
import sqlite3

from DataBase import DataBaseInterface
from GlobalData import MagicNum

class CPUserTable(DataBaseInterface.DataBaseInterface,object):
    def __init__(self):
        "初始化父类"
        super(CPUserTable,self).__init__()
    
    def CreateTable(self):
        "创建ap用户表并插入超级管理员"
        self.ExcuteCmd("CREATE TABLE CPUserTable (name TEXT PRIMARY KEY,password TEXT,ip TEXT,port INT,permission INT)")
        self.AddNewUser(['local','local','localhost',8000,MagicNum.CPUserTablec.NORMAL])
    
    def VerifyNamePsw(self,name,psw):
        "验证一个用户的用户名和密码是否正确"
        _sql = "SELECT * FROM CPUserTable where name=? AND password=?"
        _res = self.Search(_sql, [name.decode("utf8"),psw])
        if _res == []:
            return False
        else:
            return _res[0][4]
    
    def AddNewUser(self,value):
        "增加新的用户"
        try:
            self.InsertValue("CPUserTable",value)
        except sqlite3.IntegrityError:
            return False
        return True
    
    def AlterUser(self,attri,value,name):
        "更改用户信息"
        _sql = "UPDATE CPUserTable SET "+ attri +"=? where name=?"
        self.ExcuteCmd(_sql,[value,name.decode("utf8")])
    
    def searchUser(self,name):
        _sql = "SELECT * FROM CPUserTable where name=?"
        return self.Search(_sql, [name.decode("utf8")])
    
    def deleteUser(self,name):
        _sql = "DELETE FROM CPUserTable WHERE name=?"
        self.ExcuteCmd(_sql, [name.decode("utf8"),])  
    
if __name__=='__main__':
    a = CPUserTable()
    a.Connect()
    #a.deleteUser("cp")
    #a.AddNewUser(["no","no","localhost",8000,4001])
    a.AlterUser("port", 18000,"local" )
    a.CloseCon()