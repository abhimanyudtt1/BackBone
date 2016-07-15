import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class format :

    def header(self,message) :

        sys.stdout.write(bcolors.BOLD)
        sys.stdout.write('###')
        for i in range(0,len(message)):
            sys.stdout.write('#')
        sys.stdout.write('###')
        print bcolors.ENDC
        print bcolors.HEADER + ''.join(('   ',message)).upper() + bcolors.ENDC
        sys.stdout.write(bcolors.BOLD)
        sys.stdout.write('###')
        for i in range(0,len(message)):
            sys.stdout.write('#')
        sys.stdout.write('###\n')
        print bcolors.ENDC

    def info(self,message):
            sys.stdout.write("[INFO] : " )
            print bcolors.OK + str(message) + bcolors.ENDC

    def line(self,message):
            sys.stdout.write("[INFO] : " )
            print bcolors.ENDC + str(message)

    def warning(self,message) :
            sys.stdout.write("[WARNING] : " )
            print bcolors.WARNING + message + bcolors.ENDC

    def bold(self,message) :
            sys.stdout.write("[MESSAGE] : " )
            print bcolors.BOLD + message + bcolors.ENDC
    def error(self,message) :
            sys.stdout.write("[ERROR] : " )
            print bcolors.FAIL + message + bcolors.ENDC
    
    def exception(self,message,error):
            sys.stdout.write("[FAIL] : " )
            print message + " : [ " + bcolors.FAIL + error + bcolors.ENDC + " ] " 
    
    def split(self,len=150):
        sys.stdout.write("[INFO] : " )
        sys.stdout.write(bcolors.BOLD)
        for i in range(0,len):
             sys.stdout.write('#')
        print "" + bcolors.ENDC

format = format()
