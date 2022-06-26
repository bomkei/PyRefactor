

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
    while 

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


