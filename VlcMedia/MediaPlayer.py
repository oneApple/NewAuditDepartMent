# -*- coding:UTF-8 -*-   
  
import subprocess  
  
class MediaPlayer(object):  
    "利用vlc进行媒体播放"          
    def Plyaer(self,args):  
        ''' args为路径  '''    
        _cmd = "vlc" + " " + args  
        self.__p = subprocess.Popen(args = _cmd,shell=True)  
    
    def waitForProcess(self):
        self.__p.wait()
              
              
if __name__ == '__main__':
    m = MediaPlayer()
    m.Plyaer("../media/a/output.mpg")
    m.waitForProcess()
