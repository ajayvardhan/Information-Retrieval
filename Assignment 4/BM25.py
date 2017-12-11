import os
import operator
import ast
from collections import Counter
import math
from decimal import *
vocabulary = {}
uniIndex = {}
queries = {}
totalDocs = Decimal(1000)
k1 = Decimal(1.2)
k2 = Decimal(100)
b = Decimal(0.75)
totalDocLength = Decimal(0)
# create the vocabulary size dictionary
with open("vocabulary.txt") as file:
	for line in file:
		l = line.split("###")
		vocabulary[l[0]] = l[1]
		totalDocLength += Decimal(l[1])

avgDocLength = totalDocLength/totalDocs

# create the uni Index
with open("uniIndex.txt") as file:
	for line in file:
		l = line.split(" ", 1)
		uniIndex[l[0]] = l[1]

# get the queries
queryFile = raw_input("Enter the file name with the complete location that contains the queries:")
with open(queryFile) as file:
	for line in file:
		l = line.split(" ", 1)
		queries[l[0]] = l[1]

# loop through each query
for q in queries:
	queryFrequencies = Counter(queries[q].split())
	documents = {}
	rank = {}
	# for each term in the query, get the documents from the inverted index and build the dictionary with the term frequency for each term in each document
	for term in queries[q].split():
		for doc in ast.literal_eval(uniIndex[term]):
			if doc[0] in documents:
				documents[doc[0]][term] = doc[1]
			else:
				documents[doc[0]] = {}
				documents[doc[0]][term] = doc[1]

	# for each relevant document for the query, calculate the BM25
	for doc in documents:
		k = k1*((1-b)+b*(Decimal(vocabulary[doc])/avgDocLength))
		BM25 = 0
		for term in queries[q].split():
			ni = Decimal(len(ast.literal_eval(uniIndex[term])))
			if term in documents[doc]:
				fi = Decimal(documents[doc][term])
				qfi = Decimal(queryFrequencies[term])
				t1 = (Decimal(1)/((ni + Decimal(0.5))/(totalDocs - ni + Decimal(0.5))))
				t2 = ((k1+Decimal(1))*fi)/(k+fi)
				t3 = ((k2+Decimal(1))*qfi)/(k2+qfi)
				BM25 += math.log(t1*t2*t3)
			else:
				continue
			
		rank[BM25] = doc

	# output the scores to the file for each query
	rank = sorted(rank.items(), reverse = True)
	file = open(queries[q].rstrip() + ".txt", 'w')
	pageRank = 1
	for i in rank:
		if pageRank<=100:
			file.write(str(q) + " Q0 " + str(i[1]) + " " + str(pageRank) + " " + str(i[0]) + " " + "BM25\n")
			pageRank+=1
		else:
			break