from bs4 import BeautifulSoup
import requests
import time
def dfs_crawler(seed):
	links = []
	inlinks = {}
	url = "/wiki"
	# filtering out administrative links
	rejectLinks = ["/wiki/Main_Page",":","#"]
	maxLinks = 999
	maxDepth = 6
	depth = 0
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

	def crawler(start, depth):
		depth+=1
		# check if we have reached 1000 links or depth 6
		if 	depth <= maxDepth and len(links) < maxLinks:
				print "Processing links from depth: ", depth
				time.sleep(1)
				page  = requests.get(start)
				parsedPage = BeautifulSoup(page.text, "html.parser")
				for link in parsedPage.find_all('a'):
					finalLink = parseLink(link)
					if finalLink:
						if len(links) <= maxLinks:					
							if finalLink not in links:
								links.append(finalLink)
								crawler(finalLink, depth)
						else:
							break
		else:
			return None


	crawler(seed, depth)

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

	file = open('dfsoutput.txt','w')
	for i in inlinks:
		line = i + " " + ' '.join(map(str, inlinks[i]))
		file.write(line + '\n')
	file.close()

	print "Done Processing"


# seed = raw_input("Enter seed URL: ")

dfs_crawler("https://en.wikipedia.org/wiki/Tropical_cyclone")