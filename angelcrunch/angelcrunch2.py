from urllib2 import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re
import json



    
class AngelSearch(object):   

    def __init__(self, query):
        self.query = query
        tagon = (self.query.lower().replace(" ","-", ))
        self.start_url = "https://www.angellist.com/"+tagon
        print "initialising...",
        try:
            jesus_saves = open('%s.html'%tagon , 'r')
            self.raw_html =  jesus_saves.read()
            jesus_saves.close()    
            print "found written data."

        except IOError:
            print "no data found. fetching from AngelList...",
            htmlPage = urlopen(self.start_url)
            self.raw_html = htmlPage.read()
            jesus_saves = open('%s.html'%tagon , 'w')
            jesus_saves.write(self.raw_html)
            jesus_saves.close
            print "done."

        self.funding = {}
        self.founders = {}
        self.team = {}
#        self.json_stores = {}


    def get_funding(self):
    #returns a dict with info on Type, Date, Value, Investors for each Funding Round
    #updates self.funding variable  
        print "getting funding data...",
        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        key = {0:"Type", 1:"Date", 2:"Value", 3:"Investors"}
        data_store = {}
        
        l = len(mySoup.find_all('div', {"class": "section show"}))
        i = 0

        for section in mySoup.find_all('div', {"class": "section show"}): 
            u = BeautifulSoup(unicode(section))

            nameSoup = BeautifulSoup(unicode(u.find('div', {'class':'type'})))
            dateSoup = BeautifulSoup(unicode(u.find('div', {'class':"date_display"})))
            valueSoup = BeautifulSoup(unicode(u.find('div', {'class':'raised'})))
            investorsSoup = BeautifulSoup(unicode(u.find('div', {'class':'participant_list inner_section'})))         

            j= {
                key[0] : nameSoup.get_text().strip('\n'),
                key[1] : dateSoup.get_text().strip('\n'),
                key[2] : valueSoup.get_text().strip('\n'),
                key[3] : investorsSoup.get_text().strip('\n'),
                }

            data_store.update({'Round%d' % (l-i) : j})
            i +=1

        print "done"
        self.funding = data_store
        return data_store


    def get_founders(self):
    #returns a list of dicts with info on Name, Bio, and relevant Links for each Founder
    #updates self.founders variable
        print "getting founder data...",
        strainer = SoupStrainer("div", {"class": 'founders section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        key = {0:"Name", 1:"Bio", 2:"Links",}
        data_store = []

        for section in mySoup.find_all('li', {"class": "role"}):
            u = BeautifulSoup(unicode(section))

            nameSoup = BeautifulSoup(unicode(u.find('div', {'class':'name'})))
            bioSoup = BeautifulSoup(unicode(u.find('div', {'class':"bio"})))
            links = []

            for link in bioSoup.find_all('a', {'class':'at_mention_link'}):    
                links.append(link.get('href'))                   
           
            j= {
                key[0] : nameSoup.get_text().strip('\n'),
                key[1] : bioSoup.get_text().strip('\n'),
                key[2] : links,
                }

            data_store.append(j)

        print "done"
        self.founders = data_store
        return data_store


    def get_team(self):
    #returns a dict of Team roles
    #each dict returns a list of dicts with info on Name, Bio, and relevant Links for each team member
    #updates self.team variable
        
        print "getting team data...",
        strainer = SoupStrainer("div", {"class": 'section team'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        data_dict ={}

        for s in mySoup.find_all('div', {'class':'group'}):
            role = s.div.get('data-role').title()
            roleSoup = BeautifulSoup(unicode(s))
            
            if roleSoup.find('a',{'class':'view_all'}):
                print '\nlarge segment... sending to json parser',
                view_all_button = roleSoup.find('a', {'class':'view_all'})
                view_url = "https://www.angel.co"+view_all_button.get('href')
                data_dict.update({role : self.team_parser(view_url)})

            else: 

                key = {0:"Name", 1:"Bio", 2:"Links",}
                data_store = []

                for section in roleSoup.find_all('li', {"class": "role"}):
                    u = BeautifulSoup(unicode(section))

                    nameSoup = BeautifulSoup(unicode(u.find('div', {'class':'name'})))
                    bioSoup = BeautifulSoup(unicode(u.find('div', {'class':"bio"})))
                    links = []
                    
                    for link in bioSoup.find_all('a', {'class':'at_mention_link'}):    
                        links.append(link.get('href'))                   
                    
                    j= {
                        key[0] : nameSoup.get_text().strip('\n'),
                        key[1] : bioSoup.get_text().strip('\n'),
                        key[2] : links,
                        }

                    data_store.append(j)
        
                data_dict.update({role: data_store})     
                print "done"
        
        self.team = data_dict
        return data_dict


    def team_parser(self, url):
#############################################
        get_raw_data = urlopen(url)
    
#        f = open('json.html', 'r')
#        get_raw_data = f   
#############################################
        jdata = json.load(get_raw_data)


        key = {0:"Name", 1:"Bio", 2:"Links",}
        data_store = []
       
        jprofiles = jdata['startup_roles/startup_profile']
        for jp in jprofiles:
            jSoup = BeautifulSoup(jp['html'])
            
            nameSoup = BeautifulSoup(unicode(jSoup.find('div', {'class':'name'})))
            bioSoup = BeautifulSoup(unicode(jSoup.find('div', {'class':"bio"})))
            links = []
            for link in bioSoup.find_all('a', {'class':'at_mention_link'}):    
                links.append(link.get('href'))                   

            j= {
                key[0] : nameSoup.get_text().strip('\n'),
                key[1] : bioSoup.get_text().strip('\n'),
                key[2] : links,
                }

            data_store.append(j)
        return data_store


    def update(self):
        print "Requesting update..."
        tagon = self.query.lower().replace(" ","-", )
        jesus_saves = open('%s.html'%tagon , 'w')
        htmlPage = urlopen(self.start_url)
        self.raw_html = htmlPage.read()
        jesus_saves.write(self.raw_html)
        jesus_saves.close
        print "... updated and stored"
        pass
       
    def angelic(self):
        
        return {
        'Query' : self.query ,
        'Funding' : self.get_funding(),
        'Founders' : self.get_founders(),
        'Team': self.get_team(),
        }
        
        



