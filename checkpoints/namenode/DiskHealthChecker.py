from backbone import * 
import re

''' 
This is to check that SAN disk connectivity is done correctly.
This Script will check the following on a system of datanodes :
    1. Check SAN interface
    2. Check tps fs configs on datanode
    3. Check SAN memory available
'''

nodes = get_nodes_by_type('datanode')


# Checking tps fs configs
for node in nodes :


    output = node.cliCmd('show tps fs')

    if not 'Enabled: yes' in output or 'Mount point: /dev/INVALID' in output:
        directory = ['/data/']
        logger.error('%s : DN doesnot have a SAN attached or enabled.' % node.getIp())
    else :
        directory = filter(lambda x : 'Mount point:' in x , output.split('\n'))
        try :
            directory = map(lambda x : re.search('Mount point:(.*)',x).group(1),directory)
        except Exception :
            logger.error('%s : Error in parsing command :show tps fs for mount points.Please check' % node.getIp() )

    for dir in directory :
        output = node.shellCmd('df -klh | grep %s' % dir)
        out = filter(lambda x : '%' in x, output.split(' ') )
        if not len(out) == 1 :
            logger.error('%s : Error in parsing command df -klh. debug logs stdout : %s , after filter for percentage extraction passed. out = %s ' % ( node.getIp(),output,out) )
        else :
            if int(out[0][:-1]) > 95 :
                logger.error("%s : SAN disk is full: %s" % ( node.getIp(),out[0] ) )
                report.fail("%s : SAN disk is full: %s" % ( node.getIp(),out[0] ) )
            else :
                logger.info("%s : SAN disk %s full" % ( node.getIp(),out[0] ) )
                


