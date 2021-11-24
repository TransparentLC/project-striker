import fontTools.subset
import fontTools.ttLib
import glob
import os
import string

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Download from:
# https://mirrors.cloud.tencent.com/adobe-fonts/source-han-serif/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
fontPath = '../font/SourceHanSerifSC-Medium.otf'
fontSubsetPath = '../font/SourceHanSerifSC-Medium-Subset.otf'

charset = set(string.printable)
for file in glob.glob('../**/*.py', recursive=True):
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
