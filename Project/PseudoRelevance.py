from collections import Counter
import os.path

queries={}
# create a dictionary of queries to lookup later
with open("Processed Query/Query.txt",'r') as file:
	for line in file:
		query = line.split(" ", 1)
		queries[query[0]] = query[1]

with open("common_words",'r') as file:
	commonWords = file.read().split("\n")


queryFile = open("ExpandedQuery.txt",'w')
with open("Documents/cacm.rel.txt",'r') as file:
	query = ""
	frequentTerms = Counter()
	oldQuery = ""
	for line in file:
		rel = line.split()
		newQuery = rel[0]
		query = queries[newQuery].strip()
		queryList = query.split()
		if oldQuery != "" and oldQuery != newQuery:
			frequentTerms = sorted(frequentTerms.items(), key=lambda kv: kv[1], reverse=True)[:5]
			old = queries[oldQuery].strip()
			for term in frequentTerms:
				old += " " + term[0]
			queryFile.write(str(int(rel[0])-1) + " " + old + "\n")
			frequentTerms = Counter()
		doc = rel[2]
		doc = doc.split("-")[1].zfill(4)
		doc = "CACM" + "-" + str(doc) + ".html.txt"
		document = open("Processed/" + doc, 'r')
		text = document.read().split()
		text = [t for t in text if t not in commonWords]
		text = [t for t in text if t not in queryList]
		text = [t for t in text if not t.isdigit()]
		frequentTerms += Counter(text)
		document.close()
		oldQuery = newQuery
	frequentTerms = sorted(frequentTerms.items(), key=lambda kv: kv[1], reverse=True)[:5]
	old = queries[oldQuery].strip()
	for term in frequentTerms:
		old += " " + term[0]
	queryFile.write(str(rel[0]) + " " + old)
queryFile.close()
