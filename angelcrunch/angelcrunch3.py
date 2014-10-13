#angelcrunch3
#third refactored version of angel crunch with new methods.

from urllib2 import urlopen, HTTPError
from bs4 import BeautifulSoup, SoupStrainer
import re
import json
import os 
import shutil


    
class AngelSearch(object):   

    def __init__(self, query):
        

        self.query = query
        self.tagon = (self.query.lower().replace(" ","-", ))
        self.start_url = "https://www.angellist.com/"+self.tagon

        print'looking for local files...'
        if not os.path.exists('local_store/%s' %self.tagon):
            os.makedirs('local_store/%s'%self.tagon)

        try:
            with open('local_store/%s/%s.html'%(self.tagon,self.tagon),'r') as afile:
                self.raw_html =  afile.read()  

        except IOError:
            try:
                print 'getting new html from AngelList...'
                htmlPage = urlopen(self.start_url)
                self.raw_html = htmlPage.read()
                with open('local_store/%s/%s.html'%(self.tagon,self.tagon),'w') as afile:
                    afile.write(self.raw_html)

            except HTTPError, e:
                shutil.rmtree('local_store/%s' %self.tagon)
                print e

        self.funding, self.founders, self.team, self.otheragents = {}, {}, {}, {}
        self.name, self.tagline, self.product = '', '', ''
        self.tags, self.press = [], []

        self.angel = {}
        self.angelic()


    def agent_engine(self, html_sections, class_search):

        mySoup = html_sections

        data_dict = {}
        data_store = []
        i = 0
        data_role_dict = {}
        
        for agent in mySoup.find_all('ul', {'class': class_search}): 

            agent_type = agent.find_parent('div').get('data-role')

            miniSoup = agent.find_parent('div', {'data-role':agent_type})
            view_all_button = miniSoup.find('a', {'class':'view_all'})

            if view_all_button:
                view_url = "https://www.angel.co"+view_all_button.get('href')
                role_profiles = self.json_flip(view_url,agent_type)
            else:
                role_profiles = miniSoup.find_all('li', {'class', 'role'}) 

            for profile in role_profiles:
                name = profile.find('div', {'class':'name'})
                bio = profile.find('div', {'class':"bio"})
                links = []

                if not bio:
                    bio = name
                for link in bio.find_all('a', {'class':'at_mention_link'}):    
                    links.append(link.get('href'))

                j= {
                    'Name' : name.get_text(strip=True),
                    'Bio' :  bio.get_text(strip=True),
                    'Links' : links,
                    }
                
                data_store.append(j)
            data_dict.update({ agent_type.title().replace("_"," ",) : data_store})
            data_store = []
            i+= 1
             
        return data_dict

    def get_larger_agents(self):

        strainer = SoupStrainer("div", {"class": 'founders section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.founders = self.agent_engine(mySoup, 'larger roles')
        return self.founders
    
    def get_medium_agents(self):
        #get all
        strainer = SoupStrainer("div", {"class": 'past_financing section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        self.otheragents = self.agent_engine(mySoup, 'medium roles')
        return self.otheragents

    def get_team(self):

        strainer = SoupStrainer("div", {"class": 'section team'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.team = self.agent_engine(mySoup, 'medium roles')
        return self.team

    def get_name(self):

        strainer = SoupStrainer("div", {"class": 'summary'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.name = mySoup.h1.get_text()
        self.tagline= mySoup.h2.get_text()
        self.tags = []
        tag_html = mySoup.find_all( 'a', {'class':'tag'})
        for t in tag_html:
            self.tags.append(t.get_text(strip=True))

        return {'Name': self.name, 'Tagline': self.tagline, 'Tags': self.tags}

    def get_product(self):
        
        strainer = SoupStrainer('div', {'class': 'product section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        descripSouplist = mySoup.find_all('p')
        self.product = ''
        for d in descripSouplist:
            self.product = self.product+d.get_text(strip=True)+'\n'

        return {'Product' : self.product}

    def get_press(self):

        if os.path.exists('local_store/%s/activity.html' %self.tagon):
            with open('local_store/%s/activity.html' %self.tagon, 'r') as afile:
                activity_html = afile.read()
        else:
            print 'getting press html from Angellist...'
            htmlPage = urlopen(self.start_url+'/activity#press')
            with open('local_store/%s/activity.html'%self.tagon, 'w') as afile:
                activity_html = htmlPage.read()
                afile.write(activity_html)

        strainer = SoupStrainer('div', {'class':'updates'})
        mySoup = BeautifulSoup(activity_html, "html.parser", parse_only =strainer)
        
        self.press=[]
        pressSouplist = mySoup.find_all('div', {'data-tab':'press'})

        for newsSoup in pressSouplist:
            date = newsSoup.find('div', {"class":"timestamp"}).get_text(strip=True)
            site = newsSoup.find('span', {"class":"type"}).get_text(strip=True)
            url = newsSoup.find('div', {'class':'headline'}).a['href']
            headline = newsSoup.find('div', {'class':'headline'}).get_text(strip=True)
            snippet = newsSoup.find('div', {'class':'summary'}).get_text(strip=True)

            j = {'Date': date, 'Site':site, 'Link':url,
                 'Headline':headline, 'Summary':snippet}
            self.press.append(j)

        return {'Press':self.press}

    def get_funding(self):

        strainer = SoupStrainer("ul", {"class": 'startup_rounds with_rounds'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)
        
        data_dict = {}

        funding = mySoup.find_all('div', {"class": "show section"})
        i = 0

        for section in funding: 
            nameSoup = section.find('div', {'class':'type'})
            dateSoup = section.find('div', {'class':"date_display"})
            valueSoup = section.find('div', {'class':'raised'})
            investorSoup = section.find_all('div', {'class':'name'})

            keys = ['Type', 'Date', 'Value', 'Investors']
            j={}
            for souplists in [[nameSoup], [dateSoup], [valueSoup], investorSoup]:
                datalist=[]
                for soup in souplists:                      #bit of an ugly hack this to reduce lines
                    if soup:                                 #maybe just process investor Soup separately?
                        datalist.append(soup.get_text("|",strip=True))
                    else:
                        datalist = ['Unknown']
                key = keys.pop(0)
                if key != 'Investors':
                    datalist = datalist.pop()
                j.update({key : datalist})

            data_dict.update({'Round%d' % (len(funding)-i) : j})
            i +=1

        self.funding = data_dict
        return {'Funding' : self.funding}

    def update(self):

        print "Requesting update..."
        shutil.rmtree('local_store/%s' %self.tagon)
        os.makedirs('local_store/%s'%self.tagon)
        
        with open('local_store/%s/%s.html'%(self.tagon ,self.tagon), 'w') as afile:
            htmlPage = urlopen(self.start_url)
            self.raw_html = htmlPage.read()
            afile.write(self.raw_html)
        pass

    def json_flip(self, url, name):
        
        send_back_list = []
    
        try:
            jdata = json.load(open('local_store/%s/%s.json' % (self.tagon,name)))
        except IOError:
            print "fetching json data from Angellist..."
            get_raw_data = urlopen(url)
            jdata = json.load(get_raw_data)
            with  open('local_store/%s/%s.json'%(self.tagon,name), 'w') as afile: 
                afile.write(json.dumps(jdata))

        for jp in jdata['startup_roles/startup_profile']:
            send_back_list.append(BeautifulSoup(jp['html']))
        return send_back_list

    def angelic(self):
        
        self.angel = {}
        self.angel.update({'Query' : self.query})
        
        self.angel.update(self.get_name())
        self.angel.update(self.get_larger_agents())
        self.angel.update(self.get_team())
        self.angel.update(self.get_funding())
        self.angel.update(self.get_product())
        self.angel.update(self.get_press()) 
        self.angel.update(self.get_medium_agents())   
        pass


if __name__ == "__main__":
    test = AngelSearch(raw_input('Enter Name of Start Up:...'))
    print 'FOUND DATA FOR: %s' %test.name.upper()
    for k in test.angel.keys():
        print k +',',


def wipe_local_store():
    ans = raw_input("Do you want to wipe ALL locally stored data?  Y/N :")

    if ans.lower() == 'yes' or ans.lower() == 'y':
        shutil.rmtree('local_store/')











