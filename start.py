#!/usr/bin/env python

import optparse 
import sys
import re
import subprocess
import os
from backbone.format import format
currentDir = os.getcwd()
os.environ['PYTHONPATH'] = currentDir
from backbone.parser import parser
from backbone.report import report
#import backbone.report
'''
This is the start point for check pointing 
The script is a utility to run the different checks provided 
'''

def setEnv():
    currentDir = os.getcwd()
    os.environ['PYTHONPATH'] = currentDir

def print_comments(script) :
    FLAG = 0
    content = ""
    try :
        for line in open(script,'r'):
            if FLAG == 1 and not "'''" in line :
                content = content + line 
            if FLAG == 1 and "'''" in line :
                FLAG = 0
            elif FLAG == 0 and "'''" in line :
                FLAG = 1
    except IOError :
        return
    format.line(content.rstrip('\n') )


def report_fail(script,message):
    format.error(message)
    format.split()
    format.info('')
    format.info('')
    report.counter.fail()

def report_pass(script):
    format.info('Checkpoint : %s STATUS : %s' %(script,'PASSED')  )
    format.split()
    format.info('')
    format.info('')
    report.counter.Pass()

def main():

    setEnv()
    parse = optparse.OptionParser()
    parse.add_option("-f", "--flow", dest="flow",
                  help="Flow xml to define the flow in which the check points are to be run")

    parse.add_option("-c",'--check',dest='check',
                  help='To define a single checkpont script')
    parse.add_option("-t",'--testbed',dest='testbed',
                  help='To define the nodes that are to be used. It will contain the hostname,IP and type of the node available')

    parse.add_option('-v','--variable-list',dest='variable',
                  help='To define a file that will give a list of variables that may or maynot be used in the check pointing scripts')

    
    (options,args) = parse.parse_args()


    if not options.testbed :
        print "List is a mandatory field"
        print 'python ./%s --help' % sys.argv[0]
        (stdout,stderr) = subprocess.Popen('python ./%s --help' % sys.argv[0],stdout=subprocess.PIPE,stdin = subprocess.PIPE,shell = True).communicate()
        print stdout
        sys.exit(1)

    if (not options.check and options.flow ) or ( options.check and not options.flow )  :
           pass 
    else :
        print "One of the inputs is required. Either give a flow xml or give one checkpoint"
        (stdout,stderr) = subprocess.Popen('python %s --help' % sys.argv[0],stdout=subprocess.PIPE,stdin = subprocess.PIPE,shell = False).communicate()
        print stdout
        sys.exit(1)


    ipList = parser.parseTestBed(options.testbed)
    if options.flow :
        flow = parser.parseCheckpointXml(options.flow)

    else :
        flow = {}
        flow['Direct'] = options.check

    if options.variable :
        variable_dic = parser.parseVariable(options.variable)    

    else :
        variable_dic = {}

    for cls in flow :
        format.header( "Running %s type checkpoints :" % cls )
        count = 1 
        for script in flow[cls].split(','):
            format.bold("Running (%s/%s) %s" % (count,len(flow[cls].split(',')),script ) )
            count += 1
            cmd = ['python',script,"%s" % ipList,"%s" %variable_dic ]
            import time
            format.line('Log file : %s ' % '_'.join(['logs/'+'.'.join(script.split('.')[:-1]),time.strftime("%d-%m-%Y_%H-%M")]) )
            print_comments(script)
            (stdout,stderr) = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = False ).communicate()
            #print "ABC: %s , %s "% ( stdout,stderr )

            FAIL_FLAG = 0
            if stderr and not stdout:
                report_fail(script,stderr)
            elif stderr and stdout :
                for i in [ 'Traceback','error','exception','fail','No such file or directory','command not found' ] :
                    if i in stderr or i in stdout:
                        if i in stderr :
                            report_fail(script,stderr)
                            FAIL_FLAG = 1
                            break
                        else :
                            report_fail(script,stdout)
                            FAIL_FLAG = 1
                            break
                if not FAIL_FLAG :
                    report_pass(script) 
            else :
                report_pass(script)

    format.header('RESULT')
    format.info('PASSED : %s' % report.counter.getPassed() )
    format.error('FAILED : %s' % report.counter.getFailed() )




if __name__ == '__main__' :
    try :
        main()
        (stdout,stderr) = subprocess.Popen('find `pwd`/logs/ | grep  start',stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True ).communicate()
        for line in stdout.split('\n'):
            (stdout,stderr) = subprocess.Popen('rm -rf %s' % line ,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True ).communicate()
    except KeyboardInterrupt :
        print "CTRL+C pressed. Abording..."
        sys.exit(1)




