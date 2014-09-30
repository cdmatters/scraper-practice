from urllib2 import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re

    
class AngelSearch(object):
    
    def __init__(self, query):
        self.query = query
        tagon = (self.query.lower().replace(" ","-", ))
        self.start_url = "https://www.angellist.com/"+tagon
        
        print "initialising..."
        htmlPage = urlopen(self.start_url)
        self.raw_html = htmlPage.read()
        print "got data..."
        
    def raw_data(self):
        return self.raw_html            

    def get_financing(self):
        print "getting funding data...",
        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        text =  mySoup.get_text()
        
        text = text.replace("Read Press",'\n',)
        text = text.replace("Read Press",'\n',)
        r = re.compile('[\\n]*')
        
        if text:
            flist = r.split(text)
            flist.pop(-1)
            flist.pop(0)
            
            i,j,k = 0,[],{}
        
            key = {0:"Round", 1:"Date", 2:"Value", 3:"Investors"}
            while i < len(flist):
                j.append({key[i%len(key)] : flist[i]})
                i += 1
                if i%len(key) == (len(key)-1):
                    k.update({'Round%d' % (i/len(key)) : j})
                    j =[]

            print "done"
            return k
        else:
            return "\n\tError: No Funding Data"

y = raw_input('Start Up:... ')
if y:
    y= AngelSearch(y)
    print y.get_financing()



    


