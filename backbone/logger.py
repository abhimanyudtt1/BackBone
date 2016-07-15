import subprocess
import time
import sys
import re
class logger(object) :

    def __init__(self,path):
        self.logPath = path

        self.logPath = '.'.join(self.logPath.split('.')[:-1])
        self.logPath = '/'.join(('logs',self.logPath+"_"+time.strftime("%d-%m-%Y_%H-%M")))
        
        (stdout,stderr) = subprocess.Popen("ls %s" % '/'.join(self.logPath.split('/')[:-1]) , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True ).communicate()

        if stderr and not stdout :
            (stdout,stderr) = subprocess.Popen("mkdir -p %s" % '/'.join(self.logPath.split('/')[:-1]) , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True ).communicate()

        self.log = open(self.logPath,'w')
        #print self.logPath,self.log

    def info(self,message):
        timeStamp = time.strftime("%d-%m-%Y %H:%M:%S")
        self.log.write(timeStamp+" [INFO] : "+message+'\n')

    def error(self,message):
        timeStamp = time.strftime("%d-%m-%Y %H:%M:%S")
        self.log.write(timeStamp+" [ERROR] : "+message+'\n')

    def warning(self,message):
        timeStamp = time.strftime("%d-%m-%Y %H:%M:%S")
        self.log.write(timeStamp+" [WARNING] : "+message+'\n')

    def debug(self,message):
        timeStamp = time.strftime("%d-%m-%Y %H:%M:%S")
        self.log.write(timeStamp+" [DEBUG] : "+message+'\n')
logger = logger(sys.argv[0])
