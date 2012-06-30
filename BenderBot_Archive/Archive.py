from BenderBot.BenderProcess import BenderProcess
from BenderBot_Responder.Requests import Requests
from time import sleep
from re import match
from datetime import datetime

class Archive(BenderProcess):
    
    def __getMessage(self):
        self.msg = self.irc_process.queue.get()
        return self.msg
        
    def __formatMessage(self):
        self.f_msg = None
        m = match(':(.*)!.* PRIVMSG (.*) :(.*)', self.msg)
        if m:
            (nick, channel, message) = m.groups()
            if channel == self.irc.channel:
                self.f_msg = '[%s] [%s] %s' % \
                            (datetime.now().ctime(), nick, message)
        return self.f_msg
    
    def run(self):
        while True:
            if self.__getMessage():
                if self.__formatMessage():
                    # need a function that writes to text file here,
                    # we can then use that in a web interface.
                    print self.f_msg
                        
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
