from asyncio.windows_events import NULL
from liblexer import TokenKind, Token

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
  def __init__(self, tokens: list):
    self.tokens = tokens
  
  def run(self):
    i = 0

    no_bracket_tree = [
      'namespace',
      'enum',
      'struct',
      'class',
    ]

    while i < len(self.tokens):
      tok = self.tokens[i]
      
      if tok.s in no_bracket_tree:
        self.tokens[i + 1] = Token(' ')

        if self.tokens[i + 2].kind == TokenKind.Ident:
          self.tokens[i + 3] = Token(' ')
      
      i += 1
    
    return self.tokens