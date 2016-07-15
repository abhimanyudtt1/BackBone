class report(object):

    def __init__(self):
        self.counter = self.counter()

    def fail(self,msg):
    
        assert False , "%s" % msg

    class counter(object):
        
        def __init__(self):
            self._pass = 0
            self._fail = 0
        def Pass(self):
            self._pass += 1
        def fail(self):
            self._fail += 1

        def getPassed(self):
            return self._pass
        def getFailed(self):
            return self._fail

        def get(self):
            return (self._pass,self._fail)


report = report()
