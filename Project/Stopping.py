import os

with open("common_words",'r') as file:
	commonWords = file.read().split("\n")

if not os.path.exists("Stopped Corpus"):
	os.makedirs("Stopped Corpus")

for filename in os.listdir("Processed"):
	with open("Processed/" + filename,'r') as file:
		text = file.read().split()
		text = [t for t in text if t not in commonWords]
		text = ' '.join(text)
		f = open("Stopped Corpus/" + filename,'w')
		f.write(text)
		f.close()

StoppedQuery = open("StoppedQuery.txt",'w')
with open("Processed Query/Query.txt",'r') as file:
	for line in file:
		query = line.split()
		query = [q for q in query if q not in commonWords]
		query = ' '.join(query)
		StoppedQuery.write(query + "\n")
StoppedQuery.close()
