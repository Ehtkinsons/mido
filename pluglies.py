import re
import plugin_settings as pls
from plugin_settings import CHARACTER_LIMIT
from time import time
from settings import NICKNAME
from models import Sense
from string import ascii_letters
from random import choice


class Base:
    regex = '$.'

    def match(self, msg):
        if isinstance(self.regex, basestring):
            self.regex = re.compile(self.regex, re.I)

        matched = self.regex.match(msg)
        if matched:
            return list(matched.groups())

    def execute(self, *args, **kwargs):
        pass

    def respond(self, bot, channel, msg):
        if hasattr(bot, 'responded') and bot.responded:
            return
        bot.responded = True
        if msg:
            bot.msg(channel, msg)

    def run(self, bot, user, channel, msg):
        if channel == bot.nickname:
            channel = user
            if msg[:len(bot.nickname)] != bot.nickname:
                msg = "%s: %s" % (bot.nickname, msg)

        parameters = self.match(msg)
        if isinstance(parameters, list):
            self.say = lambda s: self.respond(bot, channel, s)
            self.pm = lambda s: self.respond(bot, user, s)
            self.execute(*parameters)


class Logger(Base):
    output = open(pls.Logger.output, 'a+', buffering=1)

    def execute(self, channel, user, msg):
        timestamp = int(time())
        self.output.write("%s %s %s %s\n" % (timestamp, channel, user, msg))

    def run(self, bot, user, channel, msg):
        self.execute(channel, user, msg)


class Translate(Base):
    regex = r'%s\W+translate\s+"?([^"]+)"?' % NICKNAME

    def execute(self, phrase):
        defns = (Sense.objects.filter(association__expression__text=phrase)
                              .distinct()
                              .order_by("sense_id")
                              .values_list('text', flat=True))
        if not defns:
            defns = (Sense.objects.filter(association__reading__text=phrase)
                                  .distinct()
                                  .order_by("sense_id")
                                  .values_list('text', flat=True))
        if defns:
            # a fuckin mess building the response in the allotted space
            defns = [s.split('; ') for s in defns]
            out = dict(zip(range(1, len(defns)+1), iter(lambda: [], None)))
            defns = dict(zip(range(1, len(defns)+1), defns))
            prev_s, best_s = '', ''
            while True:
                for index in out:
                    try:
                        out[index].append(defns[index].pop(0))
                    except IndexError:
                        continue

                    s = ""
                    for i, texts in out.items():
                        s = ' '.join([s,
                                      "%s." % i if texts else '',
                                      '; '.join(texts)])

                    if len(s) <= CHARACTER_LIMIT / 2:
                        best_s = str(s.strip())

                if best_s != prev_s:
                    prev_s = best_s
                else:
                    break

            if best_s:
                self.say(best_s)
            elif s:
                self.pm(s)
            else:
                self.say("I thought I knew the answer, but I forgot.")

        else:
            self.say("I don't know that.")


class Greetings(Base):
    def match(self, bot, msg):
        msg = msg.lower()
        msg = ''.join([c if c in ascii_letters else ' ' for c in msg])
        msg = [w for w in msg.split() if w.strip()]
        if len(msg) == 2 and bot.nickname in msg:
            word = [w for w in msg if w != bot.nickname][0]
            if (word in pls.Greetings.greetings or
                    word in list(pls.Greetings.appropriate)):
                return word

    def execute(self, user, word):
        if word in pls.Greetings.appropriate:
            response = pls.Greetings.appropriate[word]
        else:
            response = choice(pls.Greetings.greetings)

        if choice([True, False]):
            response = response[0].upper() + response[1:]

        punctuation = choice(['!', '', '.'])

        template = choice(['{0}: {1}{2}', '{1}, {0}{2}', '{1} {0}{2}'])
        self.say(template.format(user, response, punctuation))

    def run(self, bot, user, channel, msg):
        if channel == bot.nickname:
            channel = user
            if msg[:len(bot.nickname)] != bot.nickname:
                msg = "%s: %s" % (bot.nickname, msg)

        word = self.match(bot, msg)
        if word:
            self.say = lambda s: self.respond(bot, channel, s)
            self.execute(user, word)


class Confusion(Base):
    regex = r'%s\W+' % NICKNAME

    def execute(self):
        response = choice(pls.Confusion.expressions)
        if choice([True, False]):
            response = response[0].upper() + response[1:]
        self.say(response)
