import os
import re
from bs4 import BeautifulSoup, Comment
from collections import OrderedDict
queries={}
# create a dictionary of queries to lookup later
with open("Processed Query/Query.txt",'r') as file:
	for line in file:
		query = line.split(" ", 1)
		queries[query[0]] = query[1]

if not os.path.exists("Snippets"):
	os.makedirs("Snippets")

# stop words dictionary
with open("common_words",'r') as file:
	commonWords = file.read().split("\n")

# read the list of retreived documents for each query for BM25
for filename in os.listdir("BM25 Output"):
	with open("BM25 Output/" + filename,'r') as file:
		queryFile = open("Snippets/" + filename, 'w')
		for line in file:
			l = line.split()
			qu = queries[l[0]].split()
			query = [q for q in qu if q not in commonWords]
			f = l[2].replace(".txt","")
			if f != "Query":
				# extract the document name from each line and parse the raw document
				with open("Documents/cacm/" + f,'r') as rawFile:
					soup = BeautifulSoup(rawFile, 'html.parser')
					# split the sentences by period
					sentences = soup.pre.get_text().replace("\n"," ").split(".")
					scores = {}
					position = 0
					# for each sentence, calculate scores based on the number of times the query terms appear on it
					for sentence in sentences:
						position +=1
						score = 0
						s = sentence.split()
						for i in range(len(s)):
							if s[i].lower().strip() in query:
								score+=1
								# highlight the query term
								s[i] = "<b>" + s[i] + "</b>"
						sentence = " ".join(se for se in s)
						sentence = sentence.replace("</b> <b>", " ")
						scores[sentence] = (score,position)
					scores = sorted(scores.items(), key=lambda kv: kv[1][0], reverse=True)[:3]
					count = 0
					snippets = {}
					# get the top 3 sentences and rearrange them based on their positions in the original document
					for score in scores:
						if score[1][0] != 0:
							snippets[score[1][1]] = score[0]
					if (not snippets):
						for score in scores:
							snippets[score[1][1]] = score[0]
					snippets = sorted(snippets.items())
					snippet = ""
					# combine the sentences to create a snippet
					for snip in snippets:
						snippet += snip[1].strip() + ". "
					line = line.strip().replace("\n", "")
					line += " " + snippet + "\n"
					# write the line to a new file
					queryFile.write(line)
		queryFile.close()
