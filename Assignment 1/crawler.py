from bs4 import BeautifulSoup
import requests
import time
def crawler(seed):
	links = []
	seed = seed
	url = "/wiki"
	# filtering out administrative links
	rejectLinks = ["/wiki/Main_Page",":","#"]
	maxLinks = 1000
	maxDepth = 6
	depth = 1
	links.append(seed)
	file = open('output.txt','w')
	file.write(seed + '\n')

	# download the page and store the raw html in the output folder
	def downloadPage(link):
		rawPage  = requests.get(link)
		parsedPage = BeautifulSoup(rawPage.text, "html.parser")
		fullPage = open("Output/" + str(len(links))+'.txt','w')
		fullPage.write(link + '\n')
		fullPage.write(str(parsedPage))
		fullPage.close()

	# download the seed page first
	seedPage  = requests.get(seed)
	parsedSeedPage = BeautifulSoup(seedPage.text, "html.parser")
	downloadPage(seed)

	# crawl all the links in a single depth
	def getLinks(rawPage):
		# loop through all the anchor tags
		for link in rawPage.find_all('a'):
			tempLink = link.attrs
			if 'href' in tempLink:
				# get the link from the anchor tag
				finalLink = tempLink['href']
				if finalLink.startswith(url) and not any(word in finalLink for word in rejectLinks):
					finalLink = "https://en.wikipedia.org" + finalLink.encode('ascii','ignore')
					# if the link hasn't been processed already, add the link to the output and download
					if finalLink not in links:				
						links.append(finalLink)
						file.write(finalLink + '\n')
						downloadPage(finalLink)
						if len(links) == maxLinks:
							break
		

	for link in links:
		# check if we have reached 1000 links or depth 6
		if len(links) == maxLinks or depth > maxDepth:
			break
		else:
			print "Processing links from depth: ", depth
			time.sleep(1)
			page  = requests.get(link)
			parsedPage = BeautifulSoup(page.text, "html.parser")
			getLinks(parsedPage)
			depth+=1

	file.close()
	print "Done Processing"


seed = raw_input("Enter seed URL: ")

crawler(seed)