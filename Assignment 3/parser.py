from bs4 import BeautifulSoup, Comment
import re
import os
from collections import Counter
import operator
inputPath = raw_input("Enter the full path where the input files are located: ")
outputPath = raw_input("Enter the full path where the output files are to be generated: ")
# loop though all the files in the input folder
for filename in os.listdir(inputPath):
	file = open(inputPath + "/" + filename,'r')
	soup = BeautifulSoup(file, 'html.parser')
	# remove all the unwanted lines and extract just the text
	soup.find(id='mw-navigation').extract()
	soup.find(id='footer').extract()
	soup.find(id='siteSub').extract()
	soup.find(id='jump-to-nav').extract()	
	title = soup.title.get_text()
	output = open(outputPath + "/" + str(title.encode('ascii','ignore')).replace(" - Wikipedia", "") + '.txt','w')
	for script in soup.find_all('script'):
	    script.extract()
	for noscript in soup.find_all('noscript'):
	    noscript.extract()
	for math in soup.find_all('math'):
	    math.extract()
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	for comment in comments:
	   comment.extract()
	# write the cleansed and parsed text to the output file for each file
	for line in soup.body.get_text().split('\n'):
		s = str(line.encode('ascii','ignore')).strip()
		if s != "":
			temp = ""
			for t in s.split(" "):
				if re.match('[a-zA-Z0-9]', t):
					if not any(i.isdigit() for i in t):
						temp += re.sub('[^a-zA-Z0-9-]', '', t).lower() + " "
					else:
						temp += re.sub('[^a-zA-Z0-9-.,]', '', t) + " "
			output.write(temp + " ")
	file.close()
	output.close()

# create indexes
indexPath = outputPath
uniIndex = {}
biIndex = {}
triIndex = {}
uniTermFreq = Counter()
biTermFreq = Counter()
triTermFreq = Counter()
count = {}
#loop though the corpus created earlier
for filename in os.listdir(indexPath):
	file = open(indexPath + "/" + filename,'r')
	words = str(file.read()).split()
	uni = Counter(words)
	uniTermFreq += uni
	# calculate the 1, 2 and 3 n-gram term frequencies and document indexes
	for word in uni:
		if word in uniIndex:
			uniIndex[word].append([filename,uni[word]])
		else:
			uniIndex[word] = [[filename,uni[word]]]
	bi = Counter([i+ " " + j for i,j in zip(words[::2], words[1::2])])
	biTermFreq += bi
	for word in bi:
		if word in biIndex:
			biIndex[word].append([filename,bi[word]])
		else:
			biIndex[word] = [[filename,bi[word]]]
	tri = Counter([i+ " " + j+ " " + k for i,j,k in zip(words[::2], words[1::2], words[2::3])])
	triTermFreq += tri
	for word in tri:
		if word in triIndex:
			triIndex[word].append([filename,tri[word]])
		else:
			triIndex[word] = [[filename,tri[word]]]
	count[filename.replace(".txt", "")] = len(words)
	file.close()

# write all the indexes to the output files
file = open("uniIndex.txt",'w')
for key in sorted(uniIndex):
	file.write(str(key) + " " + str(uniIndex[key]) +"\n")
file.close()

file = open("biIndex.txt",'w')
for key in sorted(biIndex):
	file.write(str(key) + " " + str(biIndex[key]) +"\n")
file.close()

file = open("triIndex.txt",'w')
for key in sorted(triIndex):
	file.write(str(key) + " " + str(triIndex[key]) +"\n")
file.close()

file = open("uniTermFreq.txt",'w')
for key in sorted(uniTermFreq.items(), key=operator.itemgetter(1), reverse=True):
	file.write(str(key[0]) + " " + str(key[1]) +"\n")
file.close()

file = open("biTermFreq.txt",'w')
for key in sorted(biTermFreq.items(), key=operator.itemgetter(1), reverse=True):
	file.write(str(key[0]) + " " + str(key[1]) +"\n")
file.close()

file = open("triTermFreq.txt",'w')
for key in sorted(triTermFreq.items(), key=operator.itemgetter(1), reverse=True):
	file.write(str(key[0]) + " " + str(key[1]) +"\n")
file.close()

file = open("uniDocFreq.txt",'w')
for key in sorted(uniIndex):
	s = str(key)
	for i in uniIndex[key]:
		s += " " + str(i[0])
	s += " " + str(len(uniIndex[key]))
	file.write(s +"\n")
file.close()

file = open("biDocFreq.txt",'w')
for key in sorted(biIndex):
	s = str(key)
	for i in biIndex[key]:
		s += " " + str(i[0])
	s += " " + str(len(biIndex[key]))
	file.write(s +"\n")
file.close()

file = open("triDocFreq.txt",'w')
for key in sorted(triIndex):
	s = str(key)
	for i in triIndex[key]:
		s += " " + str(i[0])
	s += " " + str(len(triIndex[key]))
	file.write(s +"\n")
file.close()