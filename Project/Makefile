# define a makefile variable for the java compiler
#
JCC = javac
JC = java
PY = python
# define a makefile variable for compilation flags
# the -g flag compiles with debugging information
#
JFLAGS = -g

# JSOUP JAR
JSOUP = jsoup-1.10.3.jar

# Copy
CP = -cp

#allJars
ALL = \*
NEEDEDJARS = lucene-core-7.1.0.jar:lucene-queryparser-7.1.0.jar:lucene-analyzers-common-7.1.0.jar
RUNJARS = .:lucene-core-7.1.0.jar:lucene-queryparser-7.1.0.jar:lucene-analyzers-common-7.1.0.jar

JSOUPJAR = '.:jsoup-1.10.3.jar'

default: Task1.class Task2.class Task3.class Task4.class Task5.class Task6.class Task7.class Task8.class

Task1.class: TextProcessing.java
	@$(JCC) $(CP) $(JSOUP) $(JFLAGS) TextProcessing.java

Task2.class: TermFrequency.java
	@$(JCC) $(JFLAGS) TermFrequency.java

Task3.class: IndexCreator.java
	@$(JCC) $(JFLAGS) IndexCreator.java

Task4.class: QueryTermFrequency.java
	@$(JCC) QueryTermFrequency.java

Task5.class: BM25.java
	@$(JCC) BM25.java

Task6.class: TFIDFModel.java
	@$(JCC) TFIDFModel.java

Task7.class: QueryLikeliHoodModel.java
	@$(JCC) QueryLikeliHoodModel.java

Task8.class: Lucene.java
	@$(JCC) $(CP) $(NEEDEDJARS) $(JFLAGS) Lucene.java

 		
Phase-1-Task2:	runPseudoRelevance

Phase-1-Task3: 	runWithStopping runWithStemming

Phase-2: runSnippet

processText:
	@$(JC) $(CP) $(JSOUPJAR) TextProcessing

createIndex:
	@$(JC) IndexCreator $(Corpus)

runLucene: processText
	@$(JC) $(CP) $(RUNJARS) Lucene

runBM25:
	@$(JC) BM25 $(type)	

runTFIDF:
	@$(JC) TFIDFModel $(type)

runQueryLikeliHood:
	@$(JC) QueryLikeliHoodModel $(type)

runSnippet:
	@$(PY) SnippetGeneration.py

runWithStopping:
	@$(PY) Stopping.py

runWithStemming:
	@$(PY) StemmingParser.py

runPseudoRelevance	:
	@$(PY) PseudoRelevance.py

clean:
	@rm -rf *.class "BM25 Output" "File Size" "Inverted Indexes" "Processed" "Processed Query" "TFIDF Output" QLH* "Snippets" "Stemmed" "Stopped Corpus" "Lucene Index" "Lucene Output" "StemmedQuery.txt" "StoppedQuery.txt" "ExpandedQuery.txt"
