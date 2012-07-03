from BenderBot.BenderProcess import BenderProcess
from BenderBot_Responder.Requests import Requests
from BenderBot.Configuration import get_config
from time import sleep
from re import match
from datetime import datetime
import os

class Archive(BenderProcess):
    
    def __init__(self):
        self.config = get_config()
        try:
            self.logdir = self.config.get('Archive', 'logdir')
        except:
            self.logpath = './'
        super(Archive, self).__init__()
    
    def __getMessage(self):
        self.msg = self.irc_process.queue.get()
        return self.msg
        
    def __formatMessage(self):
        self.f_msg = None
        m = match(':(.*)!.* PRIVMSG (.*) :(.*)', self.msg)
        if m:
            (nick, channel, message) = m.groups()
            if channel == self.irc.channel:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%m')
                self.f_msg = '%s <%s> %s' % \
                            (timestamp, nick, message)
        return self.f_msg
    
    def __appendLog(self):
        d = datetime.now()
        filename = '%s-%s-%s.txt' % (d.year, d.month, d.day)
        
        # be sure our path exists
        p = os.path.expanduser(self.logdir)
        if not os.path.exists(p):
            os.makedirs(p)
        
        # append data to log
        self.logger.debug('Appending message to %s%s' % (p, filename))
        f = open('%s%s' % (p, filename), 'a+')
        f.write(self.f_msg + '\n')
        f.close()
    
    def run(self):
        while True:
            if self.__getMessage():
                if self.__formatMessage():
                    self.__appendLog()
                        
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
