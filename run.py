#!/usr/bin/python
from twisted.internet import reactor, protocol
from mido import Mido


class MidoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        p = Mido()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        print "lost connection: ", reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()


if __name__ == '__main__':
    f = MidoFactory()
    reactor.connectTCP("irc.rizon.net", 6667, f)
    reactor.run()
