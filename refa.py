import glob
from librefactor import *

dirs = [
  "test"
]

exts = [
  ".cpp",
  ".hpp",
  ".c",
  ".h"
]

files = [ ]

for i in dirs:
  for e in exts:
    files.extend(glob.glob(f'{i}/**/*{e}', recursive=True))

for i in files:
  retval = 0

  # Open
  with open(i, mode='r', encoding='utf-8') as f:
    lines = f.readlines()

    # Reduce indents
    retval = reduce_indent(lines)

    if retval[0]:
      lines = retval[1]

    lexer = Lexer(lines)
    tokens = lexer.run()

    print([t.s for t in tokens])

  # Failed to reduce indent
  if not retval[0]:
    continue

  # Write
  with open(i, mode="w") as f:
    f.writelines(retval[1])
