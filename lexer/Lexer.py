import re
import sys
from .Token import Token
from .LexerError import LexerError
from .Rules import TokenType

class Lexer:
    def __init__(self, rules, skip_whitespace=True):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('[^ \t\r\f\v]')
        self.new_line = re.compile('\n')

    def input(self, buf):
        self.buf = buf
        self.pos = 0
        self.line = 1

    def token(self):
        if(self.pos >= len(self.buf)):
            return None
        else:
            if self.skip_whitespace:
                match = self.re_ws_skip.search(self.buf, self.pos)

                if match:
                    if self.new_line.match(self.buf, self.pos):
                        while self.new_line.match(self.buf, self.pos):
                            self.pos = self.pos+1
                            self.line = self.line+1
                            pass
                        if (self.pos >= len(self.buf)):
                            return None
                        match = self.re_ws_skip.search(self.buf, self.pos)
                    self.pos = match.start()
                else:
                    return None

            match = self.regex.match(self.buf, self.pos)
            if match:
                groupname = match.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, match.group(groupname), self.line)
                if tok_type == TokenType.COMMENT:
                    self.line = self.line+1
                self.pos = match.end()
                return tok
            print(self.buf[self.pos])
            raise LexerError(self.pos, self.buf[self.line])

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok
