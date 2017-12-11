from collections import Counter
import os
import operator
indexPath = 'Output'
uniIndex = {}
biIndex = {}
triIndex = {}
uniTermFreq = Counter()
biTermFreq = Counter()
triTermFreq = Counter()
count = {}
for filename in os.listdir(indexPath):
	file = open(indexPath + "/" + filename,'r')
	words = str(file.read()).split()
	uni = Counter(words)
	uniTermFreq += uni
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

# file = open("uniIndex.txt",'w')
# for key in sorted(uniIndex):
# 	file.write(str(key) + " " + str(uniIndex[key]) +"\n")
# file.close()

# file = open("biIndex.txt",'w')
# for key in sorted(biIndex):
# 	file.write(str(key) + " " + str(biIndex[key]) +"\n")
# file.close()

# file = open("triIndex.txt",'w')
# for key in sorted(triIndex):
# 	file.write(str(key) + " " + str(triIndex[key]) +"\n")
# file.close()

# file = open("uniTermFreq.txt",'w')
# for key in sorted(uniTermFreq.items(), key=operator.itemgetter(1), reverse=True):
# 	file.write(str(key[0]) + " " + str(key[1]) +"\n")
# file.close()

# file = open("biTermFreq.txt",'w')
# for key in sorted(biTermFreq.items(), key=operator.itemgetter(1), reverse=True):
# 	file.write(str(key[0]) + " " + str(key[1]) +"\n")
# file.close()

# file = open("triTermFreq.txt",'w')
# for key in sorted(triTermFreq.items(), key=operator.itemgetter(1), reverse=True):
# 	file.write(str(key[0]) + " " + str(key[1]) +"\n")
# file.close()

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