import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import java.io.FileWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.HashMap;
/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Lucene {
    private static Analyzer analyzer = new StandardAnalyzer();
    private static Analyzer sAnalyzer = new SimpleAnalyzer();
		private static final String SYSTEM_NAME = "Lucene";
		private static String QUERY = "Processed Query/Query.txt";
		private static Map<Integer, String> queryWithId = new HashMap<>();

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException, Exception {

			Path currentRelativePath = Paths.get("");
			String str = currentRelativePath.toAbsolutePath().toString();



	//System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");
	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	//String s = br.readLine();
	String s = str + "/Lucene Index";
	Lucene indexer = null;
	try {
	    indexLocation = s;
	    indexer = new Lucene(s);
			System.out.println("Index created successfully");
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	//while (!s.equalsIgnoreCase("q")) {
	    try {
		// System.out.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		// System.out.println("[Acceptable file types: .xml, .html, .html, .txt]");
	  //   s = br.readLine();
		s = str + "/Processed";
//		if (s.equalsIgnoreCase("q")) {
//		    break;
//		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }
	//}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();


	// =========================================================
	// Now search
	// =========================================================
//	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
//		indexLocation)));
	IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexLocation))); //Modified

	IndexSearcher searcher = new IndexSearcher(reader);
	TopScoreDocCollector collector;

	// Iterate over the query file and extract the queries along with id
	File qFile = new File(QUERY);
	if (qFile.isFile()) {
		br = new BufferedReader(new FileReader(qFile));
		String line = null;
		while((line = br.readLine()) != null){
			String query_content = line.substring(2);
			String[] splits = line.split("\\s");
			int queryId = Integer.parseInt(splits[0]);
			queryWithId.put(queryId, query_content);
		}
	}

	// Start of Query Processing
	s = "";
	for(Map.Entry<Integer, String> entry:queryWithId.entrySet()) {
		collector = TopScoreDocCollector.create(100);
		int queryId = entry.getKey();
		s = entry.getValue();
		Query q = new QueryParser("contents",sAnalyzer).parse(s);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		// System.out.println("Found " + hits.length + " hits.");
		String fileName = "Lucene Output for Query "+queryId+".txt";
		File file = new File(System.getProperty("user.dir")+"/Lucene Output/"+fileName);
		if(!file.getParentFile().exists()){
				file.getParentFile().mkdirs();
		}
		if(!file.exists()){
				try {
						file.createNewFile();
				} catch (Exception e) {
						e.printStackTrace();
				}
		}
		FileWriter fileWriter = new FileWriter(file);
		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
				String docID = d.get("path");
				docID = docID.substring(docID.lastIndexOf("/")+1,docID.length());
        StringBuffer sb = new StringBuffer("");
        sb.append(String .valueOf(queryId)+" ");
        sb.append("Q0 ");
        sb.append(docID+" ");
        sb.append((i+1) + " ");
        sb.append(hits[i].score + " ");
        sb.append(SYSTEM_NAME + " ");
        fileWriter.write(sb.toString());
				fileWriter.write("\r\n");
		}
		fileWriter.flush();
		fileWriter.close();
		// 5. term stats --> watch out for which "version" of the term
		// must be checked here instead!
		Term termInstance = new Term("contents", s);
		long termFreq = reader.totalTermFreq(termInstance);
		long docCount = reader.docFreq(termInstance);
	}

	// End of Query Processing
    }

    /**
     * Constructor
     *
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    Lucene(String indexDir) throws IOException {

		//FSDirectory dir = FSDirectory.open(new File(indexDir));
	    FSDirectory dir = FSDirectory.open(Paths.get(indexDir)); //my version for 7.1.0
		IndexWriterConfig config = new IndexWriterConfig(sAnalyzer); // my version for 7.1.0

		writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     *
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
		    try {
			Document doc = new Document();

			// ===================================================
			// add contents of file
			// ===================================================
			fr = new FileReader(f);
			doc.add(new TextField("contents", fr));
			doc.add(new StringField("path", f.getPath(), Field.Store.YES));
			doc.add(new StringField("filename", f.getName(),
				Field.Store.YES));

			writer.addDocument(doc);
		    //System.out.println("Added: " + f);
	    } catch (Exception e) {
	    	//System.out.println("Could not add: " + f);
			e.printStackTrace();
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

    	//System.out.println("File is: "+file);

	if (!file.exists()) {
	    //System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
	    	addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================

	    //System.out.println(filename.endsWith(".txt"));
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
	    	queue.add(file);
	    } else {
	    	System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
}
