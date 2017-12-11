from bs4 import BeautifulSoup
import requests
import time
def bfs_crawler(seed):
	links = []
	inlinks = {}
	url = "/wiki"
	# filtering out administrative links
	rejectLinks = ["/wiki/Main_Page",":","#"]
	maxLinks = 1000
	maxDepth = 6
	depth = 1
	links.append(seed)
	inlinks[seed] = []

	def parseLink(link):
		tempLink = link.attrs
		if 'href' in tempLink:
			# get the link from the anchor tag
			finalLink = tempLink['href']
			if finalLink.startswith(url) and not any(word in finalLink for word in rejectLinks):
				finalLink = "https://en.wikipedia.org" + finalLink.encode('ascii','ignore')
				return finalLink
		return None

	# crawl all the links in a single depth
	def getLinks(parent, rawPage):
		# loop through all the anchor tags
		for link in rawPage.find_all('a'):
			finalLink = parseLink(link)
			if finalLink:
				# if the link hasn't been processed already, add the link to the output and create link in inlinks graph with parent
				# as the inlink
				if finalLink not in links:
					# inlinks[finalLink] = [parent]
					links.append(finalLink)
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
			getLinks(link, parsedPage)
			depth+=1

	count = 0
	for link in links:
		count += 1
		print count
		page  = requests.get(link)
		parsedPage = BeautifulSoup(page.text, "html.parser")
		for p in parsedPage.find_all('a'):
			finalLink = parseLink(p)
			if finalLink and finalLink in links:
				if finalLink in inlinks:
					if link not in inlinks[finalLink]:
						inlinks[finalLink].append(link)
				else:
					inlinks[finalLink] = [link]


	# output the links to a text file
	file = open('bfsoutput.txt','w')
	for i in inlinks:
		line = i + " " + ' '.join(map(str, inlinks[i]))
		file.write(line + '\n')
	file.close()

	print "Done Processing"

# seed = raw_input("Enter seed URL: ")

bfs_crawler("https://en.wikipedia.org/wiki/Tropical_cyclone")