import fontTools.subset
import fontTools.ttLib
import glob
import os
import sys
import string

globPath, fontPath, fontSubsetPath = sys.argv[1:]

charset = set(string.printable)
for file in glob.glob(globPath, recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        print('Collecting:', file)
        charset.update(f.read())
print('Charset size:', len(charset))
print(''.join(sorted(charset)))

font = fontTools.ttLib.TTFont(fontPath)
subsetter = fontTools.subset.Subsetter()
subsetter.populate(text=''.join(charset))
subsetter.subset(font)
font.save(fontSubsetPath)

print('Source font size:', os.path.getsize(fontPath))
print('Subsetted font size:', os.path.getsize(fontSubsetPath))
print(f'Reduced to {os.path.getsize(fontSubsetPath) / os.path.getsize(fontPath) * 100:.02f}%')
