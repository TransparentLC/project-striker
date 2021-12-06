import os
import random
import string

charset = string.ascii_letters + string.digits

while True:
    tag = ''.join(random.choice(charset) for x in range(8))
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'.join((
        'Generated tag:',
        '',
        f'Define: @ {tag}',
        f'Reference: @{tag}',
        '',
    )))
    input('Press enter to generate another tag. ')
