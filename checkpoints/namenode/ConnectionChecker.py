from backbone import *

'''
To check network connectivity across the cluster is fine or not. The following checks will be performed :
    1. check if 9000 port is working or not 
    2. check if 5432 port is working for pgsql
    3. 6443 port if running ( This is the feature standard port for UI )
    4. Check if the setup is keyless or not for all the datanodes to namenodes 
'''

nodes = get_nodes_by_type('namenode')

ports = get_var('ports')

for node in nodes :
    for port in ports :
        if not node.checkPort(port) :
            logger.info('%s port running on %s ' % (port,node.getIp()) )
        else :
            logger.error('%s port not running on %s ' % (port,node.getIp()) )
            report.fail('%s port not running on %s ' % (port,node.getIp()) )

dataNodes = get_nodes_by_type('datanode')

for nn in nodes :
    for dn in dataNodes :
            if not nn.isKeyless(dn.getIp() ):
                logger.error('Connection error from %s to %s' %(nn.getIp(),dn.getIp() ) )
                report.fail('Connection error from %s to %s' %(nn.getIp(),dn.getIp() ) )
            else :
                logger.info('SSH from %s and %s working correctly' %(nn.getIp(),dn.getIp() ) )

for dn in dataNodes :
    for nn in nodes :
        if not dn.isKeyless(nn.getIp() ):
            logger.error('Connection error from %s to %s' %(nn.getIp(),dn.getIp() ) )
            report.fail('Connection error from %s to %s' %(nn.getIp(),dn.getIp() ) )
        else :
            logger.info('SSH from %s and %s working correctly' %(nn.getIp(),dn.getIp() ) )







    
