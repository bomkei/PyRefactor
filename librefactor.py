from asyncio.windows_events import NULL
from enum import Enum

class TokenKind(Enum):
  TOK_DEFAULT = 0
  TOK_INT = 1
  TOK_IDENT = 2
  TOK_PUNCTUATER = 3
  TOK_OTHER = 4

# Token
class Token:
  def __init__(self):
    self.kind = TokenKind.TOK_DEFAULT
    self.pos = 0
    self.s = ''



# Lexer
class Lexer:
  # ctor
  # arg:
  #   src : list<string>  = source code
  def __init__(self, src: list):
    _src = '\n'.join(src)

    self.source = _src
    self.position = 0
    self.length = len(_src)
  
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

    punctuaters = [
      '(',
      ')',
      '{',
      '}',
      '<',
      '>',
      '[',
      ']',
    ]

    while self.check():
      ch = self.peek()
      pos = self.position
      leng = 0

      tok = Token()
      tok.pos = self.position
      tok.s = 0

      print("1")

      if ch.isdigit():
        while self.check() and self.peek().isdigit():
          leng += 1
          self.position += 1
      elif ch.isalpha() or ch == '_':
        while self.check() and (self.peek().isalnum() or self.peek() == '_'):
          leng += 1
          self.position += 1
      else:
        found = False

        for pu in punctuaters:
          if self.match(pu):
            tok.kind = TokenKind.TOK_PUNCTUATER
            tok.s = pu
            self.position += len(pu)
            found = True
            break
        
        if not found:
          print("unknown token")
          exit()

      if tok.s == 0:
        tok.s = self.source[pos:self.position]

      print("1")

      ret.append(tok)
      self.pass_space()

    return ret


# arg:
#   arr  = the source codes read by readlines()
#
# return:
#   type = tuple<bool, list<string>>
#   first value is False if failed to reduce
def reduce_indent(arr):
  ret = [ ]

  for i in arr:
    count = 0

    if i == '\n':
      ret.append(i)
      continue

    if not i.startswith('    ') and i.startswith('  '):
      return (False, [])

    for c in i:
      if c <= ' ':
        count += 1
      else:
        break

    if count == 2:
      bval1 = True
      break
    elif count == 0:
      ret.append(i)
    else:
      ret.append('  ' * int(count / 4) + i[count:])
  
  return (True, ret)


