from bs4 import BeautifulSoup
from nltk import PorterStemmer
import requests
import time

def crawler(url, keyword):
	links = []
	seed = url
	match = "/wiki"
	# filtering out administrative links
	rejectLinks = ["/wiki/Main_Page",":","#"]
	maxLinks = 1000
	maxDepth = 6
	depth = 1
	links.append(seed)
	file = open('output.txt','w')

	# download the page and store the raw html in the output folder
	def downloadPage(link):
		rawPage  = requests.get(link)
		parsedPage = BeautifulSoup(rawPage.text, "html.parser")
		fullPage = open("Output/" + str(len(links))+'.txt','w')
		fullPage.write(link + '\n')
		fullPage.write(str(parsedPage))
		fullPage.close()

	# process the seed page first
	def processSeed():
		stemmedLink = seed.replace("https://en.wikipedia.org/wiki/","")
		stemmedLink = stemmedLink.replace("_"," ")
		stemmedLink = PorterStemmer().stem(stemmedLink)
		if stemmedLink.lower().startswith(keyword) or stemmedLink.lower().endswith(" " + keyword):
			file.write(seed + '\n')
			# downloadPage(seed)
		else:
			links.remove(seed)
		

	# crawl all the links in a single depth
	def getLinks(rawPage):
		# loop through all the anchor tags
		for link in rawPage.find_all('a'):
			tempLink = link.attrs
			if 'href' in tempLink:
				# get the link from the anchor tag
				finalLink = tempLink['href']
				if finalLink.startswith(match) and not any(word in finalLink for word in rejectLinks):
					wikiLink = finalLink
					finalLink = "https://en.wikipedia.org" + finalLink.encode('ascii','ignore')
					if finalLink not in links:
						#get the stem word from the link and the title
						stemmedLink = wikiLink.replace("/wiki/","")
						stemmedLink = stemmedLink.replace("_"," ")
						stemmedLink = PorterStemmer().stem(stemmedLink)
						stemmedTitle = PorterStemmer().stem(link.text)
						# check if the stem word matches the keyword
						if stemmedLink.lower().startswith(keyword) or stemmedLink.lower().endswith(" " + keyword) or stemmedTitle.lower().startswith(keyword) or stemmedTitle.lower().endswith(" " + keyword):
							links.append(finalLink)
							file.write(finalLink + '\n')
							# downloadPage(finalLink)
							if len(links) == maxLinks:
								break
		

	for link in links:
		# check if we have reached 1000 links or depth 6
		if len(links) == maxLinks or depth > maxDepth:
			break
		else:
			if(depth == 1):
				processSeed()
			print "Processing links from depth: ", depth
			time.sleep(1)
			page  = requests.get(link)
			parsedPage = BeautifulSoup(page.text, "html.parser")
			getLinks(parsedPage)
			depth+=1

	file.close()
	print "Done Processing"

seed = raw_input("Enter seed URL: ")
keyword = raw_input("Enter the keyword: ")

crawler(seed,keyword)