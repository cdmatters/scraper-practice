#quickscript.py

#this just fetches some pages
#and loads them into a file so dont have to spend ages doing requsest
from urllib2 import urlopen


base = "https://www.angellist.com/"
json_base = "https://www.angel.co"

i = urlopen(base+'uber')
uber = i.read()

j = urlopen(base+'kivo')
kivo =j.read()

k = urlopen(base+'bucketfeet')
bucketfeet = k.read()


f = open('uber.html', 'w')
f.write(uber)
f.close

g = open('kivo.html', 'w')
g.write(kivo)
g.close

h = open('bucketfeet.html', 'w')
h.write(bucketfeet)
h.close

m = urlopen(json_base+'/startup_roles?role=employee&startup_id=19163')

n = open('json.html', 'w')
n.write(m)
n.close