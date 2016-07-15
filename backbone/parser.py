import re
import sys
import xml.etree.ElementTree as ET
import ast
class parser(object):
    def __init__(self):
        pass

    def parseCheckpointXml(self,path):

        tree = ET.parse(path)
        list = {}
        root = tree.getroot()
        assert root.tag == 'checkpoint', "Incorrect root tag, root tag should be checkpoint"
        
        for child in root.findall('class'):
            for cls in child.findall('script'):
                try :
                    list['%s' %child.attrib['name']] = '%s,%s' % (list['%s' %child.attrib['name']],cls.text )
                except Exception :
                    list['%s' %child.attrib['name']] = cls.text
        
        return list

    def parseTestBed(self,path):
        hostname = ip = type = hops = None
        node_list = []
        FH = open(path,'r')
        FIRST_TIME_FLAG = 0
            
        for line in FH :
            if line.startswith('#') :
                continue
            line = re.sub(r'[\r\s\t]+','',line)
            line = re.sub(r'^[\r\n]+$','',line)
            #print line
            if re.search(r'(?s)\[([a-zA-Z-_0-9]+)\]',line):
                if FIRST_TIME_FLAG == 0:
                    hostname = re.search(r'(?s)\[([a-zA-Z-_0-9]+)\]',line).group(1) 
                    #print "Checkpoint1"
                    FIRST_TIME_FLAG = 1
                else :
                    if None not in (hostname,ip,hops):
                        node_list.append({'ip':ip,'hostname':hostname,'type':type,'hops':hops})
                        hostname = ip = type = hops = None
                        #print "Checkpoint2"
                    else :
                        raise IndexError("Testbed parsing failed : One of the parameter is not present hostname,ip,type,hops for hostname : %s %s %s %s " % (hostname,ip,type,hops) )
                        #print "Checkpoint3"
                    hostname = re.search(r'(?s)\[([a-zA-Z-_0-9]+)\]',line).group(1)
            elif re.search(r'type=(.*)',line):
                type = re.search(r'type=(.*)',line).group(1).upper().split(',')
                #print "Checkpoint4"
            elif re.search(r'ip=(.*)',line):
                ip = re.search(r'ip=(.*)',line).group(1)
                #print "Checkpoint5"
            elif re.search(r'hops=(.*)',line):
                hops = re.search(r'hops=(.*)',line).group(1).split(',')
                #print "Checkpoint6"

        if None not in (hostname,ip,type,hops):
            node_list.append({'ip':ip,'hostname':hostname,'type':type,'hops':hops})
            hostname = ip = type = hops = None

        return node_list

    def parseVariable(self,path) :
        variable_dic = {}
        list = []
        FH = open(path,'r')
        lineCounter = 0 
        for line in FH :
            lineCounter += 1
            if line.startswith('#') or line == '\n':
                continue
            else :
                #print line
                line = re.sub('\s+','',line)
                line = re.sub('=','=[',line)
                line = re.sub('$',']',line)
                list.append( [ (i,j) for i,j in map(None,line.split('=')[0].split(','),ast.literal_eval(line.split('=')[-1])) ])

        for element in list :
            for (i,j) in element :
                variable_dic[i.lower()] = j

        #print variable_dic
        return variable_dic

                





parser = parser()
