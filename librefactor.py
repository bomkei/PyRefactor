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
    _i = i

    # 型名
    if synKind == TokenRefactor.SyntaxKind.TypeName:
      while True:
        if self.tokens[i].kind != TokenKind.Ident:
          return 0
        
        i += 1

        # テンプレート
        if self.tokens[i].s == '<':
          i += 1 # '<'

          while True:
            read = self.read_syntax(i, TokenRefactor.SyntaxKind.TypeName)

            if read == 0:
              return 0
            
            i += read
            
            if self.tokens[i].s == ',':
              i += 1
              continue
            
            break

          if self.tokens[i].s != '>':
            return 0

          i += 1 # '>'
        
        # スコープ解決演算子
        if self.tokens[i].s == '::':
          i += 1
          continue
          
        break
      
      return i - _i


  #
  # begin = index in self.tokens
  def match(self, i: int, passSpace: bool, *args) -> int:
    _b = i

    for arg in args:
      if passSpace:
        while self.tokens[i].kind == TokenKind.Space:
          i += 1

      tok = self.tokens[i]

      if type(arg) == str:
        if not tok.s == arg:
          return -1
      elif type(arg) == TokenKind:
        if not tok.kind == arg:
          return -1
      elif type(arg) == TokenRefactor.SyntaxKind:
        if self.read_syntax(i, TokenRefactor.SyntaxKind.TypeName) == 0:
          return -1
      else:
        raise ArgumentError(None, "unknown argument type")
      
      i += 1
    
    return i - _b
  
  def run(self):
    no_bracket_tree = [
      'namespace',
      'enum',
      'struct',
      'class',
    ]

    i = -1

    while True:
      i += 1
      if i >= len(self.tokens): break

      tok = self.tokens[i]

      read = 0
      bracket_count = 0

      if tok.s in no_bracket_tree:
        self.tokens[i + 1] = Token(' ')

        if self.tokens[i + 2].kind == TokenKind.Ident:
          self.tokens[i + 3] = Token(' ')
        
        continue
      
      #
      # コンストラクタ
      if (read := self.match(i, True, TokenKind.Ident, '::', TokenKind.Ident, '(')) > 0:
        i += read

        while True:
          if self.tokens[i].s == ')':
            if bracket_count == 0:
              break
            
            bracket_count -= 1
          elif self.tokens[i].s == '(':
            bracket_count += 1
          
          i += 1
        
        i += 1
        
        while self.tokens[i].s != '{':
          self.tokens.pop(i)

        self.tokens.insert(i, Token(' '))

        continue

      # 型名
      if (read := self.read_syntax(i, TokenRefactor.SyntaxKind.TypeName)) > 0:
        print(f'12455 {i}, {read}')

    return self.tokens