#prettytest.py
#this script runs the module angelcrunch2

from angelcrunch3 import AngelSearch as AS
import sys


y = raw_input('Start Up:... ')
if y:
    y= AS(y)
else:
    y = AS("uber")






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



#prettiprint(y.get_institution_investors())


y= AS("uber")
#y.update()
prettiprint(y.angelic())
#prettiprint(y.angelic())

