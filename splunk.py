import urllib
import httplib2
import time
import re
from time import localtime,strftime
from xml.dom import minidom
import json

baseurl = '***'
username = '***'
password = '***'
myhttp2 = httplib2.Http()

#Step 1: Get a session key
servercontent = myhttp2.request(baseurl + '/services/auth/login', 'POST',
                            headers={}, body=urllib.parse.urlencode({'username':username, 'password':password}))[1]



sessionkey = minidom.parseString(servercontent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
#print ("Session key: ") 
#print (sessionkey)


#Step 2: Create a search job
searchquery = 'index="_internal" | head 10'
if not searchquery.startswith('search'):
    searchquery = 'search ' + searchquery

searchjob = myhttp2.request(baseurl + '/services/search/jobs','POST',
headers={'Authorization': 'Splunk %s' % sessionkey},body=urllib.parse.urlencode({'search': searchquery}))[1]
sid = minidom.parseString(searchjob).getElementsByTagName('sid')[0].childNodes[0].nodeValue
#print ("Session id: ")
#print (sid)


#Step 3: Get the search status
myhttp2.add_credentials(username, password)
services_search_status_str = '/services/search/jobs/%s/' % sid
isNotDone = True
while isNotDone:
    searchStatus = myhttp2.request(baseurl + services_search_status_str, 'GET')[1]
    
    isDoneStatus = re.compile('isDone">(0 1)')
    
    isDoneStatus = isDoneStatus.search(searchStatus).groups()[0]
    if (isDoneStatus == '1'):
        isNotDone = False
#print ("Search status: ")
# print("isDoneStatus")
        
