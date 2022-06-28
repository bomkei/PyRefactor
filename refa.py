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
    lines = [i.rstrip() for i in f.readlines()]

    # Reduce indents
    #retval = reduce_indent(lines)
    
    #print(retval)

    #if retval[0]:
    #  lines = retval[1]

    lexer = Lexer(lines)
    tokens = lexer.run()

    ## DEBUG
    with open('tokens.txt', mode='w', encoding='utf-8') as __dbg_out:
      for tok in tokens:
        ws = ''

        if tok.s == '\n':
          ws = f'`\\n`'
        else:
          ws = f'`{tok.s}`'

        __dbg_out.write(ws + '\n')

    tokrefa = TokenRefactor(tokens)
    tokens = tokrefa.run()

  # Write
  with open(i + '.new', mode='w') as f:
    f.write(''.join([t.s for t in tokens]))
    #f.writelines(retval[1])
