import subprocess
import sys
import re
from backbone.logger import logger

class node(object) :
    '''
    This is the node class. It contains all the info of the servers. Node is the DS which stores all the info about a machine
    '''
    def __init__(self,kwargs):
        self._ip = kwargs['ip']
        self._hostname = kwargs['hostname']
        self._type = kwargs['type']
        self._topo = kwargs['hops']
        self._config = self.updateConfig()
        self._properties = {}

    def getIp(self):
        return self._ip
    def getHostname(self):
        self._hostname
    def getType(self):
        return self._type
    def getTopo(self):
        return self._topo
    def setProperty(self,property,value):
        self._properties[property] = value

    def __str__(self):
        return "%s <%s>" % (self._hostname, self._ip)

    def shellCmd(self,cmd,log = True):
        '''
        To run a shell command in the setup 
        '''
        return self.runCmd(cmd,log)

 
    def cliCmd(self,cmd,log = True):
        '''
        To run cli command
        '''
        cmd = 'echo "%s" | /opt/tms/bin/cli -m config' % cmd
        return self.runCmd(cmd,log)

    def oozieCmd(self,cmd,log = True):
        '''
        To run in oozie
        '''
        cmd = '/opt/tms/bin/pmx subshell oozie %s' % cmd
        return self.runCmd(cmd,log)
        

    def runCmd(self,cmd, log = True ): 
        '''
        Modularizing command part for cli and shell Cmd commands
        '''
        import re
        #cmd = re.sub('\$','\$',cmd) # HACK 1 TO LET THE AWK COMMANDS RUN  # Fixed properly using EOF in multiple ssh 
        cmd_init = cmd # saving just the initial command
        topo = self.getTopo()[:]
        ssh = 'ssh  -T -q -o ConnectTimeout=10 root@'
        if self.getTopo() == [] :
            cmd = "%s%s <<-'EOF'\n%s\nEOF" % (ssh,self.getIp(), cmd )
        else :
            topo.append(self.getIp() )
            i = len(topo)-1
            while not i < 0 :
                ip = topo[i]
                cmd = "%s%s <<-'EOF%s'\n%s\nEOF%s" % ( ssh,ip,i,cmd,i )
                i -= 1
        (stdout,stderr) = subprocess.Popen('%s' % cmd,stdout = subprocess.PIPE,stdin = subprocess.PIPE,shell = True).communicate()

        if log :
            logger.info('[%s] : Command : %s . stdout : %s . stderr : %s ' % ( self,cmd_init,stdout,stderr ) )
        if stderr == None :
            return stdout
        elif stdout == None :
            return stderr
        else :
            return "%s\n%s" % (stderr,stdout)

    def getConfig(self):
        return self._config
    def updateConfig(self):
        self._config = self.cliCmd('show running-config full',log = False)


    def getProperty(self,property,force = 0 ):
        try :
            if force : 
                raise KeyError
            else :
                return self._property[property]
        except (KeyError,AttributeError) as e :
            if not self.getConfig() :
                self.updateConfig()
            values = filter(lambda x : property in x ,self.getConfig().split('\n'))
            if len(values) > 1 :
                values = map(lambda x : x.split(' ')[-1],values)
                self.setProperty(property,values)
                return values
            elif len(values) == 1 :
                values = values[0].split(' ')[-1]
                self.setProperty(property,values)
                return values
            else :
                return None


    def resolveIp(self,IP = None) :
        ''' 
        To find the IP from hostname
        '''
        if not IP :
            IP = self.getIp()
        try :
            list = self.shellCmd('cat /etc/hosts | grep -i %s' % IP )
            list = re.search('([0-9.]+)\s+(.*)',list).group(2).split(' ')
        except AttributeError :
            return None 
        if len(list) >1 :
            return list
        else :
            return list[0]
            

    def resolveHostname(self,hostname) :
        '''
        To find the IP from hostname
        '''
        try :
            list = map(lambda x : re.search('([0-9.]+)\s+(.*)',x).group(1), self.shellCmd('cat /etc/hosts | grep -i %s' % hostname ).split('\n'))
        except AttributeError :
            return None
        if len(list) >1 :
            return list
        else :
            return list[0]


    def isMaster(self,log = True):
        return True if 'master'.lower() in self.cliCmd('show cluster local',log).lower() else False

    def isStandby(self,log = True):
        return False if 'master'.lower() in self.cliCmd('show cluster local',log).lower() else True

    def checkPM(self,process):
        if 'running' in self.cliCmd('show pm process %s'% process ):
            return True
        else :
            return False 

    def checkProcess(self,process):
        if self.shellCmd('ps -ef | grep -v grep | grep %s | wc -l'% process ):
            return True 
        else :
            return False

    def checkPort(self,port):
        '''
        This will check if a port is running in netstats and return 1 if its up 0 if down
        '''
        p = self.shellCmd('netstat -antp | grep %s | wc -l' % port)
        try :
            p = int(p)
        except ValueError :
            return False
        if p :
            return True
        else :
            return False
    
    def isKeyless(self,ip):
        '''
        This API will check if the current node and the IP address in the argument have keyless or not
        '''
        return not 'Permission denied' in self.shellCmd('ssh -q -o NumberOfPasswordPrompts=0  %s "echo hello"' % ip )





