import glob
from librefactor import *
from liblexer import *

dirs = [
  'test'
]

exts = [
  '.cpp',
  '.hpp',
  '.c',
  '.h'
]

files = [ ]

for i in dirs:
  for e in exts:
    files.extend(glob.glob(f'{i}/**/*{e}', recursive=True))

for i in files:
  retval = 0
  tokens = [ ]

  # Open
  with open(i, mode='r', encoding='utf-8') as f:
    lines = f.readlines()

    # Reduce indents
    retval = reduce_indent(lines)

    if retval[0]:
      lines = retval[1]

    lexer = Lexer(lines)
    tokens = lexer.run()

    tokrefa = TokenRefactor(tokens)
    tokens = tokrefa.run()

    print('\n'.join([f'`{t.s}`' for t in tokens]))

  # Write
  with open(i[:i.rfind('.')] + '.new' + i[i.rfind('.'):], mode='w') as f:
    f.write(''.join([t.s for t in tokens]))
    #f.writelines(retval[1])
