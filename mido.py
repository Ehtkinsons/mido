from twisted.words.protocols import irc
from twisted.internet import reactor
from settings import NICKNAME, NICKPASSWORD, CHANNEL, PLUGLIES
import pluglies as pl
import traceback

pluglies = [getattr(pl, p)() for p in PLUGLIES]


class Mido(irc.IRCClient):
    nickname = NICKNAME
    password = NICKPASSWORD
    channel = CHANNEL

    def signedOn(self):
        self.join(self.channel)
        if self.password:
            self.msg("NickServ", "IDENTIFY %s" % self.password)
        self.repeatingPing(59)

    def repeatingPing(self, delay):
        reactor.callLater(delay, self.repeatingPing, delay)
        self.ping(self.nickname)

    def privmsg(self, user, channel, msg):
        try:
            user, _ = user.split('!', 1)
        except ValueError:
            pass

        self.responded = False
        for p in pluglies:
            try:
                p.run(self, user, channel, msg)
            except Exception:
                traceback.print_exc()

    def connectionLost(self, reason):
        print "connection lost:", reason
        if reactor.running:
            reactor.stop()
