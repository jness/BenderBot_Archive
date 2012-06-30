from BenderBot.BenderProcess import BenderProcess
from BenderBot_Responder.Requests import Requests
from time import sleep
from re import match
from datetime import datetime
import os

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
    
    def __appendLog(self):
        d = datetime.now()
        filename = '%s-%s-%s.txt' % (d.year, d.month, d.day)
        f = open(filename, 'a+')
        f.write(self.f_msg + '\n')
        f.close()
    
    def run(self):
        while True:
            if self.__getMessage():
                if self.__formatMessage():
                    self.logger.debug('Appending message to text file')
                    self.__appendLog()
                        
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
