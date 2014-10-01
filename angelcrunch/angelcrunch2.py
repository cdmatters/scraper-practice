from urllib2 import urlopen
from bs4 import BeautifulSoup as BeautifulSoup
from bs4 import SoupStrainer
import re

    
class AngelSearch(object):   

    def __init__(self, query):
        self.query = query
        tagon = (self.query.lower().replace(" ","-", ))
        self.start_url = "https://www.angellist.com/"+tagon

        print "initialising...",
        htmlPage = urlopen(self.start_url)
        self.raw_html = htmlPage.read()
        print "got data...",
  
        self.funding = {}
        self.founders = {}
        print "initialised!"

    def get_funding(self):
        print "getting funding data...",
        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        key = {0:"Type", 1:"Date", 2:"Value", 3:"Investors"}
        data_store = {}
        
        l = len(mySoup.find_all('div', {"class": "section show"}))
        i = 0

        for section in mySoup.find_all('div', {"class": "section show"}): 
            u = BeautifulSoup(unicode(section))

            name = BeautifulSoup(unicode(u.find('div', {'class':'type'})))
            date = BeautifulSoup(unicode(u.find('div', {'class':"date_display"})))
            value = BeautifulSoup(unicode(u.find('div', {'class':'raised'})))
            investors = BeautifulSoup(unicode(u.find('div', {'class':'participant_list inner_section'})))         

            j= {
                key[0] : (name.get_text()).strip('\n'),
                key[1] : date.get_text().strip('\n'),
                key[2] : value.get_text().strip('\n'),
                key[3] : investors.get_text().strip('\n'),
                }

            data_store.update({'name%d' % (l-i) : j})
            i +=1
            j = {}
        print "done"
        self.funding = data_store
        return data_store


    def get_founders(self):
        print "getting founder data...",
        strainer = SoupStrainer("div", {"class": 'founders section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        #print mySoup
        key = {0:"Name", 1:"Bio", 2:"Links",}
        data_store = {}

        i = 1

        for section in mySoup.find_all('li', {"class": "role"}):
            u = BeautifulSoup(unicode(section))

            name = BeautifulSoup(unicode(u.find('div', {'class':'name'})))
            bio = BeautifulSoup(unicode(u.find('div', {'class':"bio"})))
            links = []
            
            for link in bio.find_all('a', {'class':'at_mention_link'}):    
                links.append(link.get('href'))                   
            
           
            j= {
                key[0] : (name.get_text()).strip('\n'),
                key[1] : (bio.get_text()).strip('\n'),
                key[2] : links,
                }

            data_store.update({'Founder%d' %  i : j})
            i +=1
            j = {}
        print "done"
        self.founders = data_store
        return data_store


    def get_employees(self):
        print "getting employee data...",
        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        key = {0:"Type", 1:"Date", 2:"Value", 3:"Investors"}
        data_store = {}
        
        l = len(mySoup.find_all('div', {"class": "section show"}))
        i = 0

        for section in mySoup.find_all('div', {"class": "section show"}): 
            u = BeautifulSoup(unicode(section))

            name = BeautifulSoup(unicode(u.find('div', {'class':'type'})))
            date = BeautifulSoup(unicode(u.find('div', {'class':"date_display"})))
            value = BeautifulSoup(unicode(u.find('div', {'class':'raised'})))
            investors = BeautifulSoup(unicode(u.find('div', {'class':'participant_list inner_section'})))         

            j= {
                key[0] : (name.get_text()).strip('\n'),
                key[1] : date.get_text().strip('\n'),
                key[2] : value.get_text().strip('\n'),
                key[3] : investors.get_text().strip('\n'),
                }

            data_store.update({'name%d' % (l-i) : j})
            i +=1
            j = {}
        print "none"
        self.funding = data_store
        return data_store





    def angelic(self):
        
        return {
        'Query' : self.query ,
        'Funding' : self.get_funding(),
        'Founder' : self.get_founders(),

        }
        
        



y = raw_input('Start Up:... ')
if y:
    y= AngelSearch(y)

    print y.get_founders()
else:
    y = AngelSearch("uber")
    print y.angelic()