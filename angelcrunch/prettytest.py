#prettytest.py
#this script runs the module angelcrunch2

from angelcrunch2 import AngelSearch
import sys


y = raw_input('Start Up:... ')
if y:
    y= AngelSearch(y)

    print y.get_team()
else:
    y = AngelSearch("uber")

    y.raw_html = open('uber.html')





def prettiprint(pretty):
    i = 0 
    for p in str(pretty):
        
        
        print p,
        sys.stdout.write('')
        if p =='['or p =='{':
            i = i + 1
            print '\n', (i*'!   '),
            sys.stdout.write('')
        
        elif p == ']'or p == '}':
            i = i - 1

            print '\n', (i*'!   '),
            sys.stdout.write('')

        elif p == ',':
     
            print '\n', (i*'!   '),
            sys.stdout.write('')

prettiprint(y.angelic())

