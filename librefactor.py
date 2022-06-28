import sys
from liblexer import TokenKind, Token
from enum import Enum

# arg:
#   lines  = the source codes read by readlines()
#
# return:
#   type = tuple<bool, list<string>>
#   first value is False if failed to reduce or already reduced
def reduce_indent(lines: list[Token]):
  ret = [ ]

  for i in range(len(lines)):
    line = lines[i]
    count = 0

    # Empty
    if line == '':
      ret.append('')
      continue

    # Already reduced
    if not line.startswith('    ') and line.startswith('  '):
      return (False, lines)

    for c in line:
      if c <= ' ':
        count += 1
      else:
        break

    indent = line[:count]
    #line = '@' * int(count / 4) + line.lstrip()
    line = line.strip()

    if ' ' in indent and '\t' in indent:
      print(f'行 {i + 1}\t: タブ文字と空白が混在しています。')

    ret.append(line)
  
  return (True, ret)

class TokenRefactor:
  class SyntaxKind(Enum):
    TypeName = 0

  # class SyntaxError(Exception):
  #   def __init__(self, msg: str):
  #     super().__init__(msg)

  def __init__(self, tokens: list):
    self.tokens = tokens
    self.indents = [ ]
    #self.it = iter(self.tokens)

  # def expect(self, i: int, s: str):
  #   if self.tokens[i] != s:
  #     raise TokenRefactor.SyntaxError(f'expected {s}')
  
  def remove_space(self, i: int) -> int:
    while True:
      tok = self.tokens[i]

      if tok.s == '\n':
        i += 1
      elif tok.kind == TokenKind.Space:
        self.tokens.pop(i)
      else:
        break
    
    return i

  def pass_space(self, i: int) -> int:
    while self.tokens[i].kind == TokenKind.Space:
      i += 1
    
    return i

  def get(self, i: int, pass_space = True) -> Token:
    while True:
      x = self.tokens[i]

      if pass_space and x.kind == TokenKind.Space:
        i += 1
      elif x.s == '@':
        self.tokens.pop(i)
      else:
        break
    
    return i, self.tokens[i]

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

    print(10001)

    for arg in args:
      i, tok = self.get(i, False)

      print(tok.s)

      if type(arg) == str:
        if tok.s != arg:
          return 0
      elif type(arg) == TokenKind:
        print(88132)
        if tok.kind != arg:
          print(1321)
          print(f'{tok.kind}, {arg}')
          return 0
      elif type(arg) == TokenRefactor.SyntaxKind:
        if self.read_syntax(i, TokenRefactor.SyntaxKind.TypeName) == 0:
          return 0
      else:
        print('passed unknown type argument to TokenRefactor::match()')
        print(f'args[{args.index(arg)}]: {type(arg)}: {arg}')
      
      i += 1
    
    return i - _b
  
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
      print(tok.s)

      read = 0
      bracket_count = 0

      #i = self.remove_space(i)

      # if tok.s == '@':
      #   tok.s = '  '
      #   continue

      if tok.s in no_bracket_tree:
        print(88918932)

        for s in no_bracket_tree:
          if (read := self.match(i, False, s, TokenKind.Space, TokenKind.Ident, TokenKind.Space, '{')) > 0:
            self.tokens[i + 1] = Token(' ')
            self.tokens[i + 3] = Token(' ')
            i += read
            break
          elif (read := self.match(i, True, s, TokenKind.Space, '{')) > 0:
            self.tokens[i + 1] = Token(' ')
            i += read
            break
        
        print(self.tokens[i].s)
        continue

      i += 1




    return self.tokens