from os import path
dirname, _ = path.split(path.abspath(__file__))


CHARACTER_LIMIT = 152


class Greetings:
    greetings = ['Welcome to the Cathedral of Shadows...', 'Greetings', 'Hello']
    appropriate = {'ping': 'pong',
                   'marco': 'polo',
                   'annyong': 'annyong',
                   }


class Logger:
    output = path.join(dirname, "plugin_data/logs.txt")


class Confusion:
    expressions = ["huh?", "what?", "eh?", "pardon?", "come again?",
                   "mmmm?", "excuse me?", "beg pardon?",
                   "hm?", "you what?",
                   "what did you just call me?"]

class DailyDemon
