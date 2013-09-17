# -*- coding: UTF-8 -*-
import sqlite3

from DataBase import DataBaseInterface

class APUserTable(DataBaseInterface.DataBaseInterface,object):
    def __init__(self):
        "初始化父类"
        super(APUserTable,self).__init__()
    
    def CreateTable(self):
        "创建ap用户表并插入超级管理员"
        self.ExcuteCmd("CREATE TABLE APUserDB (name TEXT PRIMARY KEY,password TEXT)")
        self.AddNewUser('root','root')
    
    def VerifyNamePsw(self,name,psw):
        "验证一个用户的用户名和密码是否正确"
        _sql = "SELECT * FROM APUserDB where name=? AND password=?"
        _res = self.Search(_sql, [name.decode("utf8"),psw])
        return _res != []
    
    def AddNewUser(self,name,psw):
        "增加新的用户"
        try:
            self.InsertValue("APUserDB", [name.decode("utf8"),psw])
        except sqlite3.IntegrityError,e:
            return False
        return True
    
    def AlterPsw(self,value,name):
        "更改用户密码"
        _sql = "UPDATE APUserDB SET password=? where name=?"
        self.ExcuteCmd(_sql,[value,name])
    
    def searchUser(self,name):
        _sql = "SELECT * FROM APUserDB where name=?"
        return self.Search(_sql, [name.decode("utf8")])
    
    def deleteUser(self,name):
        _sql = "DELETE FROM APUserDB WHERE name=?"
        self.ExcuteCmd(_sql, [name.decode("utf8"),])
        
    
if __name__=='__main__':
    a = APUserTable()
    a.Connect()
    #a.CreateTable()
    #a.deleteUser("any")
    a.CloseCon()