from  backbone import *
import re


'''
This will check the following :
    1. If a machine is in safeMode or not. If system is in safe mode : 
        a. Check the replication percentage
        b. Check which DNs are in unhealty state 
        c. Check the reason for unhealthy state of DNs
        
    2. Check if the File system is corupt:  
        a. Check that 
'''


nodes = get_nodes_by_type('namenode')



for node in nodes :
    if node.isMaster() :
        if 'Safe mode is OFF' == node.shellCmd('hdfs dfsadmin -safemode get'):
            logger.info('System is not in safemode. Proceeding..')
        else :
            logger.error('System is in safe mode.')
            logger.info('Now checking for replication percentage')
            logger.info('Running fsck to get report on hdfs')
            output = node.shellCmd('hdfs fsck /| tail -20')

            percentage = [i for i in output.split('\n') if 'Minimally replicated blocks' in i ]
            percentage = re.search('Minimally replicated blocks:\s+[0-9]+\s+(.*)',percentage[0]).group(1)

            logger.info('Percentage blocks replicated : %s ' % percentage )
            logger.info('Now Checking The datanodes for error.')

            output = node.shellCmd('hdfs dfsadmin -report' ).split('\n')
            DEAD_FLAG = 0
            deadDNList = []
            for line in output :
                if 'Dead datanodes' in line :
                    DEAD_FLAG = 1 
                if 'Hostname:' in line and DEAD_FLAG :
                    deadDNList.append(line.split(' ')[-1] )

            logger.info('List of dead DNs : %s ' % ','.join(deadDNList) )

            logger.info('Now checking reason for DN dead in datanode logs')

            nodes = get_nodes_by_type('datanode')

            #for node in nodes :
            #    if node.getIp() in deadDNList :
            #        # Checking in DN if space is full


            

            
nodes = get_nodes_by_type('namenode')

for node in nodes :
    if node.isMaster() :
        if 'active' in node.shellCmd('/opt/hadoop/bin/hdfs haadmin -getServiceState %s' % node.resolveIp() ).lower() :
            logger.info('%s : Node is Master node ' )
        else :
            logger.error('%s : Mater TM Node is in standby according to hadoop. Please check command /opt/hadoop/bin/hdfs haadmin -getServiceState %s ' %(node.getIp(),node.resolveIp()) )
            report.fail ( '%s : Mater TM Node is in standby according to hadoop. Please check command /opt/hadoop/bin/hdfs haadmin -getServiceState %s ' %(node.getIp(),node.resolveIp()) )
    elif node.isStandby() :
        if 'standby' in node.shellCmd('/opt/hadoop/bin/hdfs haadmin -getServiceState %s' % node.resolveIp() ).lower() :
            logger.info('%s : Node is Standby node ' )
        else :
            logger.error('%s : Mater TM Node is in Master mode according to hadoop. Please check command /opt/hadoop/bin/hdfs haadmin -getServiceState %s ' %(node.getIp(),node.resolveIp()) )
            report.fail ( '%s : Mater TM Node is in Master mode according to hadoop. Please check command /opt/hadoop/bin/hdfs haadmin -getServiceState %s ' %(node.getIp(),node.resolveIp()) )

    
