from enum import Enum
from re import T

# TokenKind
class TokenKind(Enum):
  Default = 0
  Int = 10
  Ident = 20
  Char = 21,
  String = 22,
  Punctuater = 30
  Preprocess = 31
  Comment = 32
  Space = 40
  Other = 50

# Token
class Token:
  def __init__(self, s = ''):
    self.kind = TokenKind.Default
    self.pos = 0
    self.s = s

# Lexer
class Lexer:
  # ctor
  # arg:
  #   src : list<string>  = source code
  def __init__(self, src: list):
    #_src = '\n'.join([i.rstrip() for i in src])

    #self.source = _src

    tmp = [ ]

    for _i in src:
      i = _i.rstrip()

      # ignore empty line
      if i.strip() == '':
        tmp.append('')
        continue
        

    self.source = '\n'.join(tmp)
    self.position = 0
    self.length = len(self.source)

    self.punctuaters = [
      "...",
      ">>",
      "<<",
      "+=",
      "-=",
      "*=",
      "/=",
      "%=",
      "{",
      "}",
      "(",
      ")",
      "<",
      ">",
      "[",
      "]",
      "+",
      "-",
      "*",
      "/",
      "%",
      ",",
      ".",
    ]
  
  def check(self):
    return self.position < self.length

  def peek(self):
    return self.source[self.position]

  def match(self, s):
    try:
      return self.source[self.position : self.position + len(s)] == s
    except:
      return False

  def pass_space(self):
    while self.check() and self.peek() <= ' ':
      self.position += 1

  def run(self):
    ret = [ ]
    self.pass_space()

    while self.check():
      ch = self.peek()
      pos = self.position
      leng = 0

      tok = Token()
      tok.pos = self.position
      tok.s = 0

      if ch.isdigit():
        tok.kind = TokenKind.Int
        while self.check() and self.peek().isdigit():
          self.position += 1
      elif ch.isalpha() or ch == '_':
        tok.kind = TokenKind.Ident
        while self.check() and (self.peek().isalnum() or self.peek() == '_'):
          self.position += 1
      elif ch == '"' or ch == '\'':
        self.position += 1
        tok.kind = TokenKind.Char if ch == '\'' else TokenKind.String
        begin = ch

        while self.check() and self.peek() != begin:
          if self.peek() == '\\':
            self.position += 1

          self.position += 1

        self.position += 1
      elif self.match('#'):
        self.position += 1
        tok.kind = TokenKind.Preprocess

        while self.peek() != '\n':
          self.position += 1
      elif self.match('//'):
        self.position += 2
        tok.kind = TokenKind.Comment

        while self.peek() != '\n':
          self.position += 1
      elif self.match('/*'):
        self.position += 2
        tok.kind = TokenKind.Comment

        while not self.match('*/'):
          self.position += 1

        self.position += 2
      else:
        found = False
        tok.kind = TokenKind.Punctuater

        for pu in self.punctuaters:
          if self.match(pu):
            self.position += len(pu)
            found = True
            break
        
        if not found:
          if self.peek().isspace():
            tok.kind = TokenKind.Space
            while self.check() and self.peek().isspace():
              self.position += 1
          else:
            while self.check() and (not (self.peek().isalnum() or self.peek() == '_') and self.peek() > ' '):
              self.position += 1

      tok.s = self.source[pos:self.position]
      ret.append(tok)

    return ret
