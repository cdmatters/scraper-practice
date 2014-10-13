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

        if not os.path.exists('local_store/%s' %self.tagon):
            os.makedirs('local_store/%s'%self.tagon)

        
        print "initialising...",
        try:
            jesus_saves = open('local_store/%s/%s.html'%(self.tagon,self.tagon) , 'r')
            self.raw_html =  jesus_saves.read()
            jesus_saves.close()    
            print "found local data."

        except IOError:
            print "no local data. \nfetching from AngelList...",
            try:
                htmlPage = urlopen(self.start_url)
                self.raw_html = htmlPage.read()
                jesus_saves = open('local_store/%s/%s.html'%(self.tagon,self.tagon) , 'w')
                jesus_saves.write(self.raw_html)
                jesus_saves.close
                print "done."
            except HTTPError, e:
                shutil.rmtree('local_store/%s' %self.tagon)
                print '\n',e, '[ANGELLIST PAGE NOT FOUND]'



        self.funding = {}
        self.founders = {}
        self.team = {}
        self.name = ''
        self.tagline = ''
        self.tags = []
        self.otheragents = {}
        self.angel = {}
        self.product = ''
        self.press = []


    def agent_engine(self, html_sections, class_search):
        mySoup = html_sections

        data_dict = {}
        data_store = []
        i = 0
        data_role_dict = {}

        for agent in mySoup.find_all('ul', {'class': class_search}):
             
            data_role_dict.update({ i : agent.find_parent('div').get('data-role')})
            miniSoup = agent.find_parent('div', {'data-role':data_role_dict[i]})
            view_all_button = miniSoup.find('a', {'class':'view_all'})

            if view_all_button:
                print "found view all.\n   fetching json..."
                view_url = "https://www.angel.co"+view_all_button.get('href')
                role_profiles = self.json_flip(view_url,data_role_dict[i])
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
                    'Name' : name.get_text().strip('\n'),
                    'Bio' :  bio.get_text().strip('\n'),
                    'Links' : links,
                    }
                
                data_store.append(j)
            data_dict.update({((data_role_dict[i]).title().replace("_"," ",)):data_store})
            data_store = []
            i+= 1
             
        return data_dict


    def get_medium_agents(self):
        
        print "getting institution data...",
        strainer = SoupStrainer("div", {"class": 'past_financing section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.otheragents = self.agent_engine(mySoup, 'medium roles')
        print 'done.'
        return self.otheragents


    def get_larger_agents(self):

        print "getting founder data...",
        strainer = SoupStrainer("div", {"class": 'founders section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.founders = self.agent_engine(mySoup, 'larger roles')
        print 'done.'
        return self.founders


    def get_team(self):
        print "getting team data...",
        strainer = SoupStrainer("div", {"class": 'section team'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        self.team = self.agent_engine(mySoup, 'medium roles')
        print 'done.'
        return self.team



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
        
        funding = mySoup.find_all('div', {"class": "show section"})
        i = 0

        for section in funding: 
           
            u = section

            nameSoup = u.find('div', {'class':'type'})
            dateSoup = u.find('div', {'class':"date_display"})
            valueSoup = u.find('div', {'class':'raised'})
            investorsSoup = u.find('div', {'class':'participant_list inner_section'})        

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
        shutil.rmtree('local_store/%s' %self.tagon)
        os.makedirs('local_store/%s'%self.tagon)
        
        jesus_saves = open('local_store/%s/%s.html'%(self.tagon ,self.tagon), 'w')
        htmlPage = urlopen(self.start_url)
        self.raw_html = htmlPage.read()
        jesus_saves.write(self.raw_html)
        jesus_saves.close
        print "... updated and stored"
        pass

    def json_flip(self, url, name):
        send_back_list = []
        try:
            print "   searching for local data...",
            jdata = json.load(open('local_store/%s/%s.json' % (self.tagon,name)))
            print "found..."
        except IOError:
            print "no local data.\n   fetching json data...",
            get_raw_data = urlopen(url)
            jdata = json.load(get_raw_data)
            jesus_saves = open('local_store/%s/%s.json'%(self.tagon,name), 'w') 
            jesus_saves.write(json.dumps(jdata))
            print "loaded and saved."

        
        for jp in jdata['startup_roles/startup_profile']:
            send_back_list.append(BeautifulSoup(jp['html']))
        return send_back_list


    def get_product(self):
        self.product=''
        print 'getting product description...',
        strainer = SoupStrainer('div', {'class': 'product section'})
        mySoup = BeautifulSoup(self.raw_html, "html.parser", parse_only=strainer)

        descripSouplist = mySoup.find_all('p')
        for d in descripSouplist:
            self.product = self.product+d.get_text().strip('\n')+'\n'
        print 'done'
        return self.product

    def get_press(self):
        pass



    def angelic(self):
        
        self.get_name()

        self.angel = {
        'Query' : self.query ,
        'Funding' : self.get_funding(),
        'Name': self.name,
        'Tagline' : self.tagline,
        'Tags':self.tags,
        'Product': self.get_product() 
        }

        self.angel.update(self.get_larger_agents())
        self.angel.update(self.get_team())
        self.angel.update(self.get_medium_agents())

        pass
        
    

if __name__ == "__main__":
    test = AngelSearch(raw_input('Enter Name of Start Up:...'))
    test.angelic()
    print test.angel.keys()
    print test.get_press()


def wipe_local_store():
    ans = raw_input("Do you want to wipe ALL locally stored data?  Y/N :")

    if ans.lower() == 'yes' or ans.lower() == 'y':
        shutil.rmtree('local_store/')











