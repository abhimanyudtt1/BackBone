import os
import subprocess
from backbone.nodes import node
from backbone.logger import logger
from backbone.report import report
from backbone.format import format
os.environ["PYTHONPATH"] = os.getcwd()
import sys
import ast


def get_nodes_by_type(ty):
    list = []
    for element in ast.literal_eval(sys.argv[1]) :
        #print element
        if ty.lower() in map(lambda x : x.lower(),element['type']) :
            list.append(node(element))
    return list


def get_var(var) :
    element = ast.literal_eval(sys.argv[2])
    try :
        val = element[var.lower()]
    except KeyError :
        val = None
    return val
        

#def create_node(hostname,


# Creating a logging here 


#def logger():
#    return logger.logger(sys.argv[0])


def smart_find_by_type(type) :
    '''
    This is a utill to find the nodes by type using the test bed available 
    The util provides a list of nodes that can be safely asumed to be the type of node,
    that is provided as arguemnt to the util.
    '''

    list = []

    if type.lower() == 'namenode' :
        nodes = get_nodes_by_type(type)
        if len(nodes) >= 2 :
            return nodes
        else :
            for node in nodes :
                return node.cliCmd('show cluster global')

    else :
        if type.lower() in ['psql','pgsql'] :
            '''
            Need to find the psql from namenode 
            '''
            nodes = get_nodes_by_type('namenode')
            if nodes == [] :
                return None 
            else :
                node = [ i for i in nodes if i.isMaster() ]
                node = node[0]
                try :
                    count = int(node.shellCmd('cli -m config -t \'show ru fu\' | grep -i \'parque\' | grep oozie | wc -l ') )
                except ValueError,TypeError :
                    if count > 0 :
                        pass
                        

    

            

def userInput(req):
    '''
    To ask for user input
    '''

    x = raw_input('USERINPUT: %s ' % req )
    return x.rstrip()
