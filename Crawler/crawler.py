from bs4 import BeautifulSoup
import requests
import time
links = []
seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"
seedName = "Tropical cyclone"
url = "/wiki"
rejectLinks = ["/wiki/Main_Page",":","#"]
maxLinks = 1000
maxDepth = 6
depth = 0
links.append(seed)
file = open('Output/output.txt','w')
file.write(seed + '\n')

def downloadPage(link):
	rawPage  = requests.get(link)
	parsedPage = BeautifulSoup(rawPage.text, "html.parser")
	fullPage = open('Output/' + str(len(links))+'.txt','w')
	fullPage.write(link + '\n')
	fullPage.write(str(parsedPage))
	fullPage.close()

seedPage  = requests.get(seed)
parsedSeedPage = BeautifulSoup(seedPage.text, "html.parser")
downloadPage(seed)

def getLinks(rawPage):
	for link in rawPage.find_all('a'):
		tempLink = link.attrs
		if 'href' in tempLink:
			finalLink = tempLink['href']
			if finalLink.startswith(url) and not any(word in finalLink for word in rejectLinks):
				finalLink = "https://en.wikipedia.org" + finalLink.encode('ascii','ignore')
				if finalLink not in links:				
					links.append(finalLink)
					file.write(finalLink + '\n')
					downloadPage(finalLink)
					if len(links) == maxLinks:
						break
	

for link in links:
	if len(links) == maxLinks or depth == maxDepth:
		break
	else:
		time.sleep(1)
		page  = requests.get(link)
		parsedPage = BeautifulSoup(page.text, "html.parser")
		getLinks(parsedPage)
		depth+=1

file.close()