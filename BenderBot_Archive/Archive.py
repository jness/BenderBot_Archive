from BenderBot.BenderProcess import BenderProcess
from BenderBot.Configuration import get_config
from time import sleep
from re import match
from datetime import datetime
import os
import _mysql

class Archive(BenderProcess):
    
    def __init__(self):
        self.config = get_config()
        super(Archive, self).__init__()
    
    def __getMessage(self):
        # get() is blocking so we don't need a sleep in our loop
        self.msg = self.queue.get()
        return self.msg
        
    def __formatMessage(self):
        self.f_msg = None
        m = match(':(.*)!.* PRIVMSG (.*) :(.*)', self.msg)
        if m:
            (nick, channel, message) = m.groups()
            if channel == self.irc.channel:
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.f_msg = (timestamp, nick, message)
        return self.f_msg
    
    def __appendLog(self):
        # get our log dir
        try:
            self.logdir = self.config.get('Archive', 'logdir')
        except:
            self.logpath = './'
            
        d = datetime.now()
        filename = '%s-%s-%s.txt' % (d.year, d.month, d.day)
        
        # be sure our path exists
        p = os.path.expanduser(self.logdir)
        if not os.path.exists(p):
            os.makedirs(p)
        
        # append data to log
        self.logger.debug('Appending message to %s%s' % (p, filename))
        f = open('%s%s' % (p, filename), 'a+')
        f.write('%s <%s> %s\n' % self.f_msg)
        f.close()
        
    def __connectDB(self):
        self.options = dict(self.config.items('Archive'))
        self.conn = _mysql.connect(host=self.options['host'],
                                   port=int(self.options['port']),
                                   user=self.options['user'],
                                   passwd=self.options['password'],
                                   db=self.options['database'])
        self.__checkDBTable()
        
    
    def __checkDBTable(self):
        q = ("""CREATE TABLE IF NOT EXISTS %s 
               (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `message` longtext NOT NULL, `user` varchar(75) NOT NULL,
                `created` datetime NOT NULL, PRIMARY KEY (`id`)
               )
            """ % self.options['table'])
        self.conn.query(q)
        
    def __writeDB(self):
        self.__connectDB()
        q = ("INSERT INTO %s (user, message, created) VALUES ('%s', '%s', NOW())" \
                % (self.options['table'], self.f_msg[1], self.f_msg[2]))
        self.conn.query(q)
    
    def run(self):
        while True:
            if self.__getMessage():
                if self.__formatMessage():
                    if self.config.getboolean('Archive', 'db_enable'):
                        self.__writeDB()
                    else:
                        self.__appendLog()
