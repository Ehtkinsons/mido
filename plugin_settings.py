from os import path
dirname, _ = path.split(path.abspath(__file__))


CHARACTER_LIMIT = 152


class Greetings:
    greetings = ['hi', 'hello', 'hey', 'sup', 'yo', 'hola']
    appropriate = {'ping': 'pong',
                   'marco': 'polo',
                   'annyong': 'annyong',
                   }


class Logger:
    output = path.join(dirname, "plugin_data/logs.txt")


class Confusion:
    expressions = ["huh?", "what?", "eh?", "pardon?", "come again?",
                   "sorry, what?", "excuse me?", "I beg your pardon?",
                   "could you run that by me again?", "you what?",
                   "What did you just call me?"]
