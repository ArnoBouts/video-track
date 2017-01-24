import threading

class Com(threading.Thread):

    def __init__(self, camera):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.camera = camera
        self.msgToSend = None

    def goto(self, goto):
        self.msgToSend = goto

    def run(self):
        i = 0
        while not self._stopevent.isSet():
            self.readMsg()
            if(not self.msgToSend is None):
                self.sendMsg()
                self.msgToSend = None
            self._stopevent.wait(.05)

    def sendMsg(self):
        print(bin(self.msgToSend))

    def stop(self):
        self._stopevent.set( )

    def readMsg(self):
        return
