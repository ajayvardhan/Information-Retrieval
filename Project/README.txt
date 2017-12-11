Installations:
  To install python-pip enter the ` sudo apt-get install python-pip`
  To install bsoup enter the command `pip install beautifulsoup4` in terminal

To Compile All Files:
  Enter the Command `make` in terminal.

To Execute Phase 1:
  Task 1: Enter `make processText` which will do the text processing and store
           the result in Processed dir and query is stored in Processed Query dir.
           To create inverted index enter `make createIndex Corpus="Default"` which
           will generate the inverted index in the Inverted Indexes directory.

           Part A)
           To run the BM25 model enter the command `make runBM25 type="Default"`
           To run the TFIDF model enter the command `make runTFIDF type="Default"`
           To run the QueryLikelihood model enter the command `make runQueryLikeliHood type="Default"`

           Part B)
           To run the Lucene enter the command `make runLucene` in terminal.

  Task 2: To run the pseudo-relevance and generate the expanded query enter the
          command `make runPseudoRelevance` in the terminal.
          To run the expanded query on BM25 enter the command `make runBM25 type="PR"`
          in terminal.

  Task 3:  Enter the command `make Phase-1-Task3` in terminal

          To run the stopped
          `make createIndex Corpus="Stopped"`

          BM25 enter the command `make runBM25 type="STOPPED"` and
          To run the stopped version on TFIDF enter the command

          `make runTFIDF type="STOPPED"` in terminal.
          To run the stopped version on QueryLikeliHoodModel enter the command
          `make runQueryLikeliHood type="STOPPED"` in terminal.

          `make createIndex Corpus="Stemmed"`
          BM25 enter the command `make runBM25 type="STEMMED"` in terminal.
          TFIDF  enter the command `make runTFIDF type="STEMMED"` in terminal.
          QueryLikeliHoodModel enter the command `make runQueryLikeliHood type="STEMMED"` in terminal


Phase 2:
         To run the phase 2 enter the command
         `make processText`
         `make createIndex Corpus="Default"`
         `make runBM25 type="Default"`
         `make Phase-2` in terminal.

Phase 3:



clean: Enter `make clean` to delete all the created output directories.
