from backbone import *
import re
'''
To check if the following config files are correctly set :
    1. editservicecli.properties
    2. editservice.properties
    3. ibpublisher.properties
'''    

nodes = get_nodes_by_type('rubix')
nn_nodes = get_nodes_by_type('namenode')


nn_ips = map(lambda x : x.getIp(),nn_nodes )
nn_nodes = filter(lambda x : x.isMaster(log = False) ,nn_nodes )
nn_node = nn_nodes[0]

out = nn_node.cliCmd('show cluster configured' ).split('\n')
out = filter(lambda x : 'Cluster master virtual IP address' in x , out )[0]
vip = re.search('\s+Cluster master virtual IP address:\s([0-9\.]+)',out).group(1)

nameservice = nn_node.shellCmd('pmx subshell hadoop_yarn show config ' ).split('\n')

nameservice = filter(lambda x : 'nameservice' in x , nameservice )[0]

nameservice = nameservice.split(' ')[-1]



file_location = { 'editservicecli.properties' : '/opt/tms/ib-framework/editservice/config/core/editservicecli.properties',
                  'editservice.properties':'/opt/tms/ib-framework/editservice/config/core/editservice.properties',
                  'ibpublisher.properties': '/opt/tms/ib-framework/editservice/config/core/ibpublisher.properties' }


for node in nodes :
    for k,v in file_location.iteritems() :
        logger.info('%s : Now checking file %s. Location : %s ' %( node,k,v) )

        output = node.shellCmd('cat %s' % v )
        ERROR_FLAG = 0
        for line in output.split('\n') :
            if 'postgresHost' in line :
                if not vip in line :
                    logger.error('%s,%s : postgresHost not configured properly. Actual : %s , Expected : %s ' % (node,v,line,vip) )
                    ERROR_FLAG = 1
            if 'ibFsNameservice' in line :
                if not nameservice in line :
                    logger.error('%s,%s : ibFsNameservice not configured properly. Line : %s and value required is %s' % (node,v,line,nameservice) )
                    ERROR_FLAG = 1

            if 'ibFsNamenodes' in line :
                ips = line.split('=')[-1].split(',')
                for ip in ips :
                    if not ip in nn_ips:
                        logger.error('%s,%s : ibFsNamenodes not configured properly. Required nodes : %s and property set to %s ' % (node,v,ips,nn_ips) )
                        ERROR_FLAG = 1

            if 'rmiRegistryHost' in line :
                if not node.getIp() in line :
                    logger.error('%s,%s : rmiRegistryHost not configured properly. Value set to %s, expected value : %s ' % (node,v,line,node.getIp() ) )
                    ERROR_FLAG = 1

            if 'restMachineUrl' in line :
                port = line.split(':')[-1]
                property = filter(lambda x : 'editservice' in x , filter(lambda x : 'redirect' in x , node.cliCmd('show running-config full',log = False).split('\n')) )[-1].split(' ')[-1]
                if not property == port :
                    logger.error('%s,%s : restMachineUrl not configured properly. Actual Value : %s ,Expected : %s ' % (node,v,property,port) )
                    ERROR_FLAG = 1
                
                host = line.split(':')[-2].lstrip('/').lstrip('/')
                if re.search('[0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3}',host ) :
                    if not vip in line :
                        logger.error('%s : restMachineUrl not configured properly. Actual Value : %s ,Expected : %s ' %(node,v,line,vip) )
                        ERROR_FLAG = 1
                        

            if ERROR_FLAG :
                report.fail('Problem found in editservice properties. Please Check logs for details' )


                
    
 
