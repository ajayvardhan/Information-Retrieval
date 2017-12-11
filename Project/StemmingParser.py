import os

if not os.path.exists("Stemmed"):
    os.makedirs("Stemmed")

with open("Documents/cacm_stem.txt",'r') as file:
	docs = file.read().strip().replace("\n"," ").split("#")
	for d in docs[1:]:
		document = d.strip().split()
		filename = document[0].strip()
		f = open("Stemmed/D" + filename + ".txt",'w')
		f.write(' '.join(document[1:]))

StemmedQuery = open("StemmedQuery.txt", "w")
with open("Documents/cacm_stem.query.txt",'r') as file:
	count = 1
	for line in file:
		line = str(count) + " " + line
		StemmedQuery.write(line)
		count+=1
StemmedQuery.close()
