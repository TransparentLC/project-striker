import os
import subprocess
import sys

subprocess.Popen((
    'cwebp',
    '-q', '100',
    '-z', '9',
    '-m', '6',
    '-mt',
    '-lossless',
    sys.argv[1],
    '-o', f'{os.path.splitext(sys.argv[1])[0]}.webp',
)).wait()