from BenderBot.BenderProcess import BenderProcess
from BenderBot_Responder.Requests import Requests
from time import sleep
from re import match
from datetime import datetime

class Archive(BenderProcess):
    
    def run(self):
        while True:
            msg = self.irc_process.output.recv()
            if msg:
                m = match(':(.*)!.* PRIVMSG (.*) :(.*)', msg)
                if m:
                    (nick, channel, message) = m.groups()
                    # be sure this is a channel message
                    if channel == self.irc.channel:
                        print '[%s] [%s] %s' % (datetime.now().ctime(),
                                               nick, message)
                        
            sleep(0.02) # Slow down the loop just a bit to avoid CPU melt ;)
