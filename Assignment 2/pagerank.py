from decimal import *
import math
import operator
inlinks = {}
outlinks = {}
PR = {}
newPR = {}
d = Decimal(0.85)
entropy = Decimal(0)
perplexity = Decimal(0)
count = Decimal(0)
oldPerplexity = Decimal(0)
inlinksFile = raw_input("Enter the file with full path that contains the inlinks graph: ")

# parse the graph and create the inlinks and pagerank dicts
with open(inlinksFile) as file:
	for line in file:
		page = [p.rstrip() for p in line.split(" ")]
		for p in page:
			if p not in PR:
				PR[p] = 0
		inlinks[page[0]] = list(set(page[1:]))
		# remove the page itself from the inlinks
		if page[0] in inlinks[page[0]]:
			inlinks[page[0]].remove(page[0])


# find outlinks count for each page
for i in inlinks:
	for p in inlinks[i]:
		if p in outlinks:
			outlinks[p].append(i)
		else:
			outlinks[p] = [i]

totalPages = Decimal(len(PR))

for i in outlinks:
	if i in outlinks[i]:
		outlinks[i].remove(i)


# create the sink list
sink = list(set(PR.keys())-set(outlinks.keys()))

# initialise pagerank to 1/N
for p in PR:
	PR[p] = Decimal(Decimal(1)/Decimal(totalPages))
# iteratively calculate pagerank
while(True):
	# check perplexity to exit loop
	if Decimal(oldPerplexity) - Decimal(perplexity) < 1:
		count+=1
	else:
		count = 0
	if count == 4:
		break

	# calculate sink pagerank
	sinkPR = Decimal(0)
	for s in sink:
		sinkPR += PR[s]

	# calculate the new page rank for each page
	for p in PR:
		newPR[p] = (Decimal(1) - d)/totalPages
		newPR[p] += d*sinkPR/totalPages
		for q in inlinks[p]:
			newPR[p] += d*PR[q]/Decimal(len(outlinks[q]))

	# update pagerank and calculate new entropy and perplexity
	entropy = 0
	for p in PR:
		PR[p] = newPR[p]
		entropy += newPR[p]*Decimal(math.log(newPR[p],2))

	oldPerplexity = perplexity
	perplexity = math.pow(Decimal(2),-entropy)

sortedPR = sorted(PR.items(), key=operator.itemgetter(1), reverse=True)

# print the pages and their pageranks to the output file
file = open('G2_PR.txt','w')
# count = 0
for i in sortedPR:
	# if count == 50:
	# 	break
	line = i[0] + " " + str(i[1])
	file.write(line + '\n')
	count += 1
file.close()