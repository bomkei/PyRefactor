from argparse import ArgumentError, ArgumentTypeError
from asyncio.windows_events import NULL
from lib2to3.pgen2 import token
from liblexer import TokenKind, Token
from enum import Enum

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

class TokenRefactor:
  class SyntaxKind(Enum):
    TypeName = 0

  # class SyntaxError(Exception):
  #   def __init__(self, msg: str):
  #     super().__init__(msg)

  def __init__(self, tokens: list):
    self.tokens = tokens
    #self.it = iter(self.tokens)

  # def expect(self, i: int, s: str):
  #   if self.tokens[i] != s:
  #     raise TokenRefactor.SyntaxError(f'expected {s}')
  
  def read_syntax(self, i: int, synKind: SyntaxKind) -> int:
    # 型名
    if synKind == TokenRefactor.SyntaxKind.TypeName:
      while True:
        if self.tokens[i] != TokenKind.Ident:
          return False
        
        i += 1

        # テンプレート
        if self.tokens[i].s == '<':
          i += 1 # '<'

          while True:
            read = self.read_syntax(i, TokenRefactor.SyntaxKind.TypeName):

            if read == 0:
              return False
            
            if self.tokens[i] == ',':
              i += 1
              continue
            
            break

          if self.tokens[i] != '>':
            return False

          i += 1 # '>'
        
        # スコープ解決演算子
        if 


  #
  # begin = index in self.tokens
  def match(self, begin: int, passSpace: bool, *args) -> int:
    _b = begin

    for arg in args:
      res = False

      if passSpace:
        while self.tokens[begin].kind == TokenKind.Space:
          begin += 1

      tok = self.tokens[begin]

      if type(arg) == str:
        if not tok.s == arg:
          return False
      elif type(arg) == TokenKind:
        if not tok.kind == arg:
          return False
      elif type(arg) == TokenRefactor.SyntaxKind:
        if not self.
      else:
        raise ArgumentError(None, "unknown argument type")
      
      begin += 1
    
    return begin - _b
  
  def run(self):
    no_bracket_tree = [
      'namespace',
      'enum',
      'struct',
      'class',
    ]

    i = 0

    while i < len(self.tokens):
      tok = self.tokens[i]

      if tok.s in no_bracket_tree:
        self.tokens[i + 1] = Token(' ')

        if self.tokens[i + 2].kind == TokenKind.Ident:
          self.tokens[i + 3] = Token(' ')
      
      #
      # コンストラクタ
      if self.match(i, True, TokenKind.Ident, '::', TokenKind.Ident, '('):

        pass

      i += 1

    return self.tokens