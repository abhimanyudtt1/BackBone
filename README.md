# BackBone
Backend automation framework
List of APIs exposed to user

    def getIp(self)
	    The getIP is a node API which returns IP attribute of the node object
	    eg : node.getIP() will return 192.168.112.72

    def getHostname(self)
	    The getHostname is a node API which returns hostname attribute of the node object
	    node.getHostname() will return NRMCA-NN1


    def getType(self)
	    To get the node type. Output will be a list.
	    node.getType() will return ['collector','namenode','acume']


    def getTopo(self)
	    Internal command Not required directly. It returns the hops from the local node on which backbone is running to connect to the final server. Used in case of a multi hop environment


    def setProperty(self,property,value)
	Internal command Not required directly. Used to set a property and value in an internally maintained dictionary to store any values required to be used during run time of a test script


    def shellCmd(self,cmd,log = True)
	Used to get output of a shell command. It returns stdout in case there is no standard error and it returns stderr in case there is no standard output. In case a command give stderr and stdout both,
    A string containing stderr followed by stdout is returned


    def cliCmd(self,cmd,log = True)
	Used to get output of a cli command. It returns stdout in case there is no standard error and it returns stderr in case there is no standard output. In case a command give stderr and stdout both, A
    string containing stderr followed by stdout is returned


    def runCmd(self,cmd,name, log = True )
	Internal command Not required directly. Used to get output of a shell command or a cli command. It returns stdout in case there is no standard error and it returns stderr in case there is no
    standard output. In case a command give stderr and stdout both, A string containing stderr followed by stdout is returned


    def getConfig(self)
	Returns full cli config of a node. The cli config is not fresh, it is the config stored at the time of node object creation


    def updateConfig(self)
	Gets fresh cli running-config and stores it as an attribute.


    def getProperty(self,property,force = 0 ):
	Parses the cli config and gets the property string being searched for and returns its value . Also stores the value for any future reference. The force argument forces a new cli config to be fetched
    from node and then doing a search on it.


    def isMaster(self)
	Checks if current node is master and returns True or false accordingly


    def isStandby(self)
	Checks if current node is standby and returns True or false accordingly


    def checkPM(self,process)
	Checks if a pm process is running on the given node


    def checkPort(self,port):
	Checks if a given port is active and listening on the given node


    def isKeyless(self,ip)
	This API will check if the current node and the IP address in the argument have keyless or not
