from backbone import *
from backbone.collector import *
import time
import re
'''
To check if the following on collector nodes :
    1. Check if kfps of collector is contant for configured days or for 5 days default
    2. Check if kfps of collector is contant for configured hours or for 10 hours default
'''    
nodes = get_nodes_by_type('collector')


for node in nodes :
    if node.isMaster(log=False):
        instance = get_instance(node)
        adaptors = get_adaptors(node,instance)
        counts = {}
        counts = dict([ ('1-day',get_var('day-count') if get_var('day-count') else 5),('1-hour',get_var('hour-count') if get_var('hour-count') else 10 ) ])
        deviationThreshold = get_var('deviationThreshold') if get_var('deviationThreshold') else 10        
        stats = {}
        for adaptor in adaptors :
            for count in counts :
                logger.info('Daily Stats being calculated now' if 'day' in count else 'Hourly Stats being calculated now')
                dayStats = node.cliCmd('collector stats instance-id %s adaptor-stats %s total-flow interval-type %s interval-count %s ' % ( instance,adaptor,count,counts[count] ) )

                logger.info('Stats have be retrieved. Calculating the mean deviation' )
                # using mean deviation to calculate this 
                for line in dayStats.split('\n'):
                    try :
                        line = re.sub('\s+',' ',line)
                        #logger.info('ABC : %s ' % line.split(' ') )
                        stats[int(line.split(' ')[0])] = int(line.split(' ')[3])
                    except (ValueError,IndexError) as e:
                        continue 
                logger.info('Stats : %s ' % stats )
                mean = reduce(lambda x,y : x+y, stats.values() )/len(stats.values())

                logger.info('Mean avg : %s' % reduce(lambda x,y : x+y, stats.values() ) )

                stats = dict(map(lambda (y,x) : (y,(abs(x-mean)/float(x))*100),stats.iteritems() ))
                logger.info('Stats : %s ' % stats )
                logger.info('Threshold variation level: %s' % deviationThreshold )
                for k,v in enumerate(stats.values()) :
                    if v > deviationThreshold :
                        logger.error('Collector deviation seen in kfps is more than %s percent : %s ' % (deviationThreshold,v )  )
                        report.fail('Collector deviation seen in kfps is more than %s percent : %s ' % (deviationThreshold,v ) )
                
                logger.info('Collector kfps correctly maintained')

            

