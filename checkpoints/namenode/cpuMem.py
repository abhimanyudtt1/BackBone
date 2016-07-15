from backbone import * 
import re
'''
To check if the cpu and memory usages of the nodes are in optimal ranges 
'''

nodes = get_nodes_by_type('namenode')
nodes_data = get_nodes_by_type('datanode')


all_nodes = nodes + nodes_data
percentage = {}
for node in nodes :
    for line in node.shellCmd('free').split('\n'):
        if 'Mem:' in line :
            search = re.search('Mem:\s+([0-9]+)\s+([0-9]+).* ',line)
            total = search.group(1)
            used = search.group(2)
            percentage[node.getIp()] = float(float(used)/float(total))*100
        else :
            pass
        
for i in percentage :
    logger.info('%s Memory utilization : %s' % (i,percentage[i]) )
    if percentage[i] > 95 :
        logger.error ( '%s Memory utilization : %s { THIS IS TOO HIGH }' % (i,percentage[i]) )    
        report.fail('%s Memory utilization : %s { THIS IS TOO HIGH }' % (i,percentage[i]) )



for i in nodes :
    for line in node.shellCmd('mpstat').split('\n'):
        if 'all' in line.lower() :
            logger.info('%s CPU utilization : %s' % (node.getIp(),line.split()[2] ) )
            if float(line.split()[2]) > 90 :
                logger.error('%s CPU utilization : %s { THIS IS TOO HIGH }' % (node.getIp(),line.split()[2] ) )
                report.fail('%s CPU utilization : %s { THIS IS TOO HIGH }' % (node.getIp(),line.split()[2] ))
