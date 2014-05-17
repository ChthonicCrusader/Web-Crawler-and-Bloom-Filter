####################################################################
##this program allows you to crawl the web site www.catchpoint.com upto two levels.
##you can change this setting by modifying the level variable in getlinks() function
##you can change the web page to be crawled by modifying the parameters of crawl() function inside main. 



#this function is used to get all the links in the mentioned web page
import urllib2

def getlinks(myurl):
	response=urllib2.urlopen(myurl)
	mylist=response.read()
	startpos=0
	url=[]
	level=0
	while startpos!=-1:
		startpos=mylist.find("a href=",startpos)
		if startpos==-1 or level>=3:
			return url
		else:
			startq=mylist.find('"http',startpos)
			endq=mylist.find('"',startq+1)
			l=mylist[startq+1:endq]
			if l[0] =='/':# first character is a  slash,add at the end of link
				l=myurl.append(l)#concatenation operator for strings instead
				url.append(l)
			elif l[0]=="#":
				pass
			else:
				url.append(l)
			startpos=endq+1
		level=level+1
##################################################################

#Listname is essentially is the record of keyword and corresponding url
def addindex(listname,keyword,urll):
	for present in listname:
		if present[0]==keyword:	## if the keyword is present in our index list, then append/add the new url
			present[1].append(urll)
			return

	listname.append([keyword,[urll]])


#################################################################

#returns the union of two lists passed as arguments
def union(a,b):
	return list(set(a)|set(b))

#################################################################

#If crawled, we will not crawl again, else will crawl and add it to the crawled list.
def crawl(n_url):
	tocrawl=getlinks(n_url)
	crawled=[]
	while tocrawl:
		try:
			n_url=tocrawl[0]
			if n_url in crawled:
				del tocrawl[0]
			else:
				got_content=get_page(n_url)
				add_page_to_index(index,n_url,got_content)
				crawled.append(n_url)
				temp_list=[]
				temp_list=getlinks(n_url)
				tocrawl=union(tocrawl,temp_list) 
				del tocrawl[0]
		except urllib2.HTTPError:
			print "errrrrr"
			crawled.append(n_url)
			del tocrawl[0]
	print index
	print "\n\n"
	
		
################################################################

#does the hashing using bloom filter
from pybloom import BloomFilter

global myurl
myurl=[]
global filters
filters={}

def add_page_to_index(index,url,content):	
	words=content.split()
	filters[url]=BloomFilter(capacity=20000,error_rate=0.9)

	for word in words:
		filters[url].add(word)
	myurl.append(url)
	print filters


################################################################
#used for lookup of keywords
import os
import re
def searchstring(st):
	words=st.split()
	for u in myurl:
		if all(w in filters[u] for w in words):
				print u
	
################################################################

#reads the contents of the web page
def get_page(url):
	import nltk
	from urllib import urlopen

	html=urlopen(url).read()
	raw=nltk.clean_html(html)
	return raw

###############################################################

global index
index={}
def main():
#	crawl("http://www.webpagetest.org/")
	crawl("http://www.catchpoint.com/")
	option='y'
	while(option=='y'):
		hell=raw_input("Enter keyword:")
		searchstring(hell)
		option=raw_input("\tDo you want to continue?y/n:")

if __name__=='__main__':
	main()
	














