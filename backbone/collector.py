import re
from backbone import node
from backbone import logger
from backbone import report


def get_adaptors(node,instance) :

        ''' 
        To find all adaptors assosiated to a given instance
        '''

        config = node.cliCmd('show running-config full',log=False).split('\n')
        config = filter(lambda x : 'collector' in x , config )
        config_adaptor = filter(lambda x : 'add-adaptor' in x , config )
        try :
            adaptors = map(lambda x : re.search('modify-instance %s add-adaptor ([a-zA-Z0-9_\-]+) type'% instance,x).group(1),config_adaptor )
        except AttributeError :
            logger.error ( '%s : Config cannot be extracted for the collector.please check' % node )
            report.fail('%s : Config cannot be extracted for the collector.please check' % node )
        logger.info('%s : Adaptors configured %s ' % (node , adaptors ))
        return adaptors

def get_instance(node) :
        '''
        To get the instance details that is currntly running on the setup 
        '''


        config = node.cliCmd('show running-config full',log=False).split('\n')
        config = filter(lambda x : 'collector' in x , config )
        config_instance = filter(lambda x : 'add-instance' in x , config )
        try :
            instance = map(lambda x : re.search('add-instance ([a-zA-Z0-9_\-]+)',x).group(1),config_instance )
        except AttributeError :
            logger.error ( '%s : Config cannot be extracted for the collector.please check' % node )
            report.fail( '%s : Config cannot be extracted for the collector.please check' % node)
        logger.info('%s : Instances configured %s ' % (node,instance ))
        if len(instance) > 1 :

            pm_result = node.cliCmd('show pm process collector',log=False ).split('\n')
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
        return instance
