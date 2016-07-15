from backbone import *

'''
To check if the following processes are running on the node or not :
    1. tps
    2. pgsql
    3. namenode daemon
    4. journal node daemon
'''    

nodes = get_nodes_by_type('namenode')

for node in nodes :
    for process in get_var('nn_processes'):
        if node.checkProcess(process) :
            logger.info('%s : %s process running' % (node,process) )
        else :
            logger.error('%s : %s process not running' % ( node,process) )
            report.fail('%s : %s process not running' % ( node,process) )
        

for node in nodes :
    for process in get_var('nn_pm_processes'):
        if node.checkPM(process) :
            logger.info('%s Running on machine %s ' % (process,node.getIp()) )
        else :
            logger.error('%s process is not running' % process)
            report.fail('%s process is not running' % process)


