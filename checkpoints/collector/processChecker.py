from backbone import *
import time
import re
'''
To check if the following processes are running on collector node node or not :
    1. collector process
    2. samplicator process
    3. Check if data is comming continuously
    4. Check if data is being dropped 
'''    
nodes = get_nodes_by_type('collector')

for node in nodes :
    for process in get_var('coll_processes'):
        if node.checkProcess(process) :
            logger.info('%s : %s process running' % (node,process) )
        else :
            logger.error('%s : %s process not running' % ( node,process) )
            report.fail('%s : %s process not running' % ( node,process) )
        

for node in nodes :
    for process in get_var('coll_pm_processes'):
        if node.checkPM(process) :
            logger.info('%s Running on machine %s ' % (process,node.getIp()) )
        else :
            logger.error('%s process is not running' % process)
            report.fail('%s process is not running' % process)


for node in nodes :
    logger.info('%s : IsMaster : %s ' % (node,node.isMaster()) )
    if node.isMaster():
        config = node.cliCmd('show running-config full').split('\n')
        config = filter(lambda x : 'collector' in x , config )
        config_adaptor = filter(lambda x : 'add-adaptor' in x , config )
        config_instance = filter(lambda x : 'add-instance' in x , config )

        try :
            adaptors = map(lambda x : re.search('add-adaptor ([a-zA-Z0-9_\-]+) type',x).group(1),config_adaptor )
        except AttributeError :
            logger.error ( '%s : Config cannot be extracted for the collector.please check' % node )
            report.fail('%s : Config cannot be extracted for the collector.please check' % node )
        
        try :
            instance = map(lambda x : re.search('add-instance ([a-zA-Z0-9_\-]+)',x).group(1),config_instance )
        except AttributeError :
            logger.error ( '%s : Config cannot be extracted for the collector.please check' % node )
            report.fail( '%s : Config cannot be extracted for the collector.please check' % node)

        


        logger.info('%s : Instances configured %s ' % (node,instance ))
        logger.info('%s : Adaptors configured %s ' % (node , adaptors ))
        

        if len(instance) > 1 :

            pm_result = node.cliCmd('show pm process collector' ).split('\n')
            pm_result = filter(lambda x : 'Argv:' in x , pm_result )
            try :
                instance = map(lambda x : re.search('(.*) -t ([0-9])',x).group(1),pm_result )
                instance = pm_result[0]
            except AttributeError :
                logger.error ( '%s : Config cannot be extracted for the collector.please check' % node )            
                logger.info('%s : Taking instance as 1 by default' % node )
                instance = 1
        else :
            instance = instance[0]

        for adaptor in adaptors :
            output = node.cliCmd('collector stats instance-id %s adaptor-stats %s total-flow' % (instance,adaptor) )
            output = int(output)
            time.sleep(3)
            output2 = node.cliCmd('collector stats instance-id %s adaptor-stats %s total-flow' % (instance,adaptor) )
            output2 = int(output2)

            if output - output2 < 0 :
                logger.info('%s : Collector receiving data for adaptor : %s ' % (node,adaptor))
            else :
                logger.error('%s : Collector NOT receiving any data for adaptor : %s ' % ( node,adaptor))
                report.fail('%s : Collector NOT receiving any data for adaptor : %s ' % (node,adaptor))


            output = node.cliCmd('collector stats instance-id %s adaptor-stats %s dropped-flow' % (instance,adaptor) )
            output = int(output)
            time.sleep(3)
            output2 = node.cliCmd('collector stats instance-id %s adaptor-stats %s dropped-flow' % (instance,adaptor) )
            output2 = int(output2)

            if output - output2 < 0 :
                logger.error('%s : Collector data getting dropped.Please check var log content below :' % (node))
                logger.error('%s' % node.shellCmd('cat /var/log/messages | grep "from collector"') )
            else :
                logger.info('%s : Collector data being processed correctly for adaptor : %s ' % (node,adaptor))
