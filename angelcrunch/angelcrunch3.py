#angelcrunch3
#third refactored version of angel crunch with new methods.

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
            jesus_saves = open('local_store/%s.html'%tagon , 'r')
            self.raw_html =  jesus_saves.read()
            jesus_saves.close()    
            print "found local data."

        except IOError:
            print "no local data. \nfetching from AngelList...",
            htmlPage = urlopen(self.start_url)
            self.raw_html = htmlPage.read()
            jesus_saves = open('local_store/%s.html'%tagon , 'w')
            jesus_saves.write(self.raw_html)
            jesus_saves.close
            print "done."

        self.funding = {}
        self.founders = {}
        self.team = {}
        self.name = ''
        self.tagline = ''
        self.tags = []
        self.otheragents ={}


    def agent_engine(self, html_sections, class_search):
        mySoup = html_sections

        data_dict = {}
        data_store = []
        i = 0
        data_role_dict = {}

        for agent in mySoup.find_all('ul', {'class': class_search}):
             
            data_role_dict.update({ i : agent.find_parent('div').get('data-role')})
            miniSoup = agent.find_parent('div', {'data-role':data_role_dict[i]})
            
            for profile in miniSoup.find_all('li', {'class', 'role'}):
                name = profile.find('div', {'class':'name'})
                bio = profile.find('div', {'class':"bio"})
                links = []

                if not bio:
                    bio = name
                for link in bio.find_all('a', {'class':'at_mention_link'}):    
                    links.append(link.get('href'))

                j= {
                    'Name' : name.get_text().strip('\n'),
                    'Bio' :  bio.get_text().strip('\n'),
                    'Links' : links,
                    }

                data_store.append(j)
            data_dict.update({((data_role_dict[i]).title().replace("_"," ", )) : data_store})

            i+= 1
        self.otheragents = data_dict    
        return data_dict


    def get_medium_agents(self):
        
        print "getting institution data...",
        strainer = SoupStrainer("div", {"class": 'past_financing section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        return self.agent_engine(mySoup, 'medium roles')


    def get_larger_agents(self):

        print "getting founder data...",
        strainer = SoupStrainer("div", {"class": 'founders section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        return self.agent_engine(mySoup, 'larger roles')


    def get_team(self):
        print "getting team data...",
        strainer = SoupStrainer("div", {"class": 'section team'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        return self.agent_engine(mySoup, 'medium roles')



    def get_name(self):
        print "getting name data...",
        strainer = SoupStrainer("div", {"class": 'summary'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        data_dict = {}

        self.name = mySoup.h1.get_text()
        self.tagline= mySoup.h2.get_text()
        tag_html = mySoup.find_all( 'a', {'class':'tag'})
        for t in tag_html:
            self.tags.append(t.get_text())
        print "done."
        return {'Name': self.name, 'Tagline': self.tagline, 'Tags': self.tags}


    def get_funding(self):
    #returns a dict with info on Type, Date, Value, Investors for each Funding Round
    #updates self.funding variable  
        print "getting funding data...",
        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        data_dict = {}
        
        funding = mySoup.find_all('div', {"class": "section show"})
        i = 0

        for section in funding: 
            u = BeautifulSoup(unicode(section))

            nameSoup = BeautifulSoup(unicode(u.find('div', {'class':'type'})))
            dateSoup = BeautifulSoup(unicode(u.find('div', {'class':"date_display"})))
            valueSoup = BeautifulSoup(unicode(u.find('div', {'class':'raised'})))
            investorsSoup = BeautifulSoup(unicode(u.find('div', {'class':'participant_list inner_section'})))         

            j= {
                "Type" : nameSoup.get_text().strip('\n'),
                "Date" : dateSoup.get_text().strip('\n'),
                "Value" : valueSoup.get_text().strip('\n'),
                "Investors" : investorsSoup.get_text().strip('\n'),
                }

            data_dict.update({'Round%d' % (len(funding)-i) : j})
            i +=1

        print "done"
        self.funding = data_dict
        return data_dict

    def update(self):
        print "Requesting update..."
        tagon = self.query.lower().replace(" ","-", )
        jesus_saves = open('local_store/%s.html'%tagon , 'w')
        htmlPage = urlopen(self.start_url)
        self.raw_html = htmlPage.read()
        jesus_saves.write(self.raw_html)
        jesus_saves.close
        print "... updated and stored"
        pass

    def angelic(self):
        
        self.get_name()

        return {
        'Query' : self.query ,
        'Funding' : self.get_funding(),
        'Founders' : self.get_larger_agents(),
        'Team': self.get_team(),
        'Name': self.name,
        'Tagline' : self.tagline,
        'Tags':self.tags, 
        'Institutions/Investors' : self.get_medium_agents()
        }











