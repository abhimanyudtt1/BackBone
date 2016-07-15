from backbone import *
import re
import os
import time
'''
To check if the base job is running continuously and with similar timings 
'''    

nodes = get_nodes_by_type('namenode')


jobStats = {}
for node in nodes :
    if node.isMaster(log = False ):
        for job in get_var('basejobs'):
            output = node.oozieCmd('show coordinator RUNNING jobs' ).split('\n')
            output = filter(lambda x : job in x ,output )
            
            logger.info('AAA %s : %s' % (job,output ))
            if len(output) >1 :
                for line in output:
                    logger.info(line)
                    line = re.sub('\t', ' ',line)
                    if job in line.split(' ') :
                        jobid = line.split(' ')[0]

            else :
                jobid = re.sub('\s+' , ' ',output[0]).split(' ')[0]
                
    
            logger.info('%s : Job id : %s ' % (job,jobid) )
            # job Id found now checking the job statistics 
            
            output = node.oozieCmd('show job %s ' % jobid )
            
            output = filter(lambda x : jobid in x ,output.split('\n') )
            output = output[1:]
            for line in output:
                line = re.sub('\t' , ' ', line ).split(' ')
                for k,v in enumerate(line) :
                    logger.info('k,v : %s,%s ' %(k,v) )
                os.environ['TZ']=line[11]
                startTime = int(time.mktime(time.strptime('%s %s' % (line[9],line[10] ) ,'%Y-%m-%d %H:%M:%S') ))
                endTime = int(time.mktime(time.strptime('%s %s' % (line[15],line[16] ) ,'%Y-%m-%d %H:%M:%S') ))
                jobStats['%s:%s:%s' % (job,jobid,line[1])] = '%s,%s '% (endTime - startTime,line[14] )


            logger.info('Job stats for job : %s : \n %s ' % ( job,jobStats ) )
            
            stats = {}
            stateStats = {}
            for k,v in enumerate(jobStats ) :
                stats[v.split(':')[-1]] = jobStats[v].split(',')[0] 
                stateStats[v.split(':')[-1]] = jobStats[v].split(',')[-1][3:] 


            logger.info('State of iterations :\n%s ' % stateStats )
            for k in stateStats :
                if 'KILL' in k or 'FAIL' in k :
                    logger.error('%s : Itreation number %s is getting killed please check. ' % ( job, k ) )


            stats = dict(map(lambda (x,y) : (x,int(y)) , stats.iteritems() ) )
            logger.info('AAAAAA : %s' % stats ) 
            mean = reduce(lambda x,y : x+y, stats.values() )/len(stats.values())

            logger.info('Mean avg : %s' % reduce(lambda x,y : x+y, stats.values() ) )

            for (k,v) in stats.iteritems() :
                if v == 0 :
                    stats[k] = 0
                else :
                    stats[k] = (abs(v-mean)/float(v))*100

            logger.info('XXXX %s ' % stats ) 
            ERROR_FLAG = 0
            for v in stats.values() :
                if v > int(get_var('job_time_threshold' )) :
                    logger.error ( 'Deviation from threshold seen in job: %s. Mean : %s and percentage deviation(%%) : %s ' % (job,mean,v) )
                    ERROR_FLAG = 1
                else :
                    logger.info('No deviation seen for job : %s ' % job ) 

            if ERROR_FLAG :
                report.fail('Deviation seen in job run timmings. Job : %s ' % job ) 
