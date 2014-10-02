from urllib2 import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import re
import json



    
class AngelSearch(object):   

    def __init__(self, query):
        self.query = query
        tagon = (self.query.lower().replace(" ","-", ))
        self.start_url = "https://www.angellist.com/"+tagon


##################################################
#        print "initialising...",
#        htmlPage = urlopen(self.start_url)
#        self.raw_html = htmlPage.read()
#        print "got data...",

        f = open('uber.html', 'r')
        self.raw_html = f.read()
##################################################

  
        self.funding = {}
        self.founders = {}
        self.team = {}




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

        i = 1

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

            data_store.append({'Founder%d' %  i : j})
            i +=1
            
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
                print 'large segment... sending to parser'
                v = roleSoup.find('a', {'class':'view_all'})
                json_url = "https://www.angel.co"+v.get('href')
                print json_url
                self.team_json(json_url)
                data_dict.update({'Role': 'json'})

            else: 

                key = {0:"Name", 1:"Bio", 2:"Links",}
                data_store = []

                i = 1

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
                    
                    i +=1
                data_dict.update({role: data_store})     
                print "done"
        
        self.team = data_dict
        return data_dict


    def team_json(self, url):
#############################################
#        output = urlopen(url)
    
        f = open('json.html', 'r')
        output = f   
#############################################


        data = json.load(output)

        print data.keys()
        data2 = data['startup_roles/startup_profile']
        for d in data2:
            print d.keys()
            print d['html']
        return None



       


    def angelic(self):
        
        return {
        'Query' : self.query ,
        'Funding' : self.get_funding(),
        'Founders' : self.get_founders(),
        'Team': self.get_team(),
        }
        
        



y = raw_input('Start Up:... ')
if y:
    y= AngelSearch(y)

    print y.get_team()
else:
    y = AngelSearch("uber")

print y.angelic()