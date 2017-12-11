import java.util.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.TreeMap;
import java.util.Comparator;
import java.util.Collections;
import java.util.Set;
import java.util.HashSet;

public class TFIDFModel{


  // TODO: PROPOSED ALGORITHM
  // Reference: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
  // 1. Find tf using unigram file and wordcount
  // 2. Use Term Freq. adjusted by document length = f / number of words in d
  // 3.


  // MAGIC CONSTANTS
	private static String QUERY = "Processed Query/Query.txt";
	private static String DOCUMENTS = "Documents/cacm";
	private static String UNIGRAM = "Inverted Indexes/Unigram";
	private static String DOCUMENTLENGTH = "File Size/wordcount";
	private static String NI = "File Size/NI";
	private static double AVG_LEN = 0.0;
	private static int N = 1000;
	private static String DELIMITER = "##";
	private static double k1 = 1.2;
	private static double b = 0.75;
	private static double k2 = 100;
	private static final String SYSTEM_NAME = "TFIDF";
	private static String STOPPED_QUERY = "StoppedQuery.txt";
	private static String STEMMED_QUERY = "StemmedQuery.txt";
	private static String EXPANDED_QUERY = "ExpandedQuery.txt";
	private static String SELECTED_QUERY = QUERY; // Default is query

	private static HashMap<Integer, String> document_id = new HashMap<>();
	private static HashMap<String, Integer> document_with_length = new HashMap<>();
	private static HashMap<String, Integer> queryWithFrequency = new HashMap<>();
	private static HashMap<String, String> qtermsIList = new HashMap<>();
	private static HashMap<String, Integer> fileCountforTerm = new HashMap<>();



  public static void main(String args[]) throws IOException{

		String input = args[0];
		System.out.println("input is "+args[0]);
	 	if(input.equals("PR")){
			SELECTED_QUERY = EXPANDED_QUERY;
		}else if(input.equals("STEMMED")){
			SELECTED_QUERY = STEMMED_QUERY;
		}else if(input.equals("STOPPED")){
			SELECTED_QUERY = STOPPED_QUERY;
		}

		// Fetch the total number of documents in collection
		File folder = new File(DOCUMENTS);
		File[] listOfFiles = folder.listFiles();
		N = listOfFiles.length;
		System.out.println("N is: " +N);

		// Find No of documents in which each term occurs
		BufferedReader bufferedReader = new BufferedReader(new FileReader(NI));
		String read = null;
		while((read = bufferedReader.readLine()) != null) {
			String[] split = read.split("\\s");
			if(split.length >= 2){
				String term = split[0];
				int ni_count = Integer.parseInt(split[1]);
				fileCountforTerm.put(term, ni_count);
			}
		}
		bufferedReader.close();

		// Start processing the queries
		BufferedReader br = new BufferedReader(new FileReader(SELECTED_QUERY));
		String li = null;
		while((li = br.readLine()) != null){
			TreeMap<String, Double> tfidf = new TreeMap<String, Double>();
			String[] split = li.split("\\s");
			String queryId = split[0].trim();
			Set<String> queryTerms = new HashSet<>();

			for(int i=1;i<split.length;i++){
				queryTerms.add(split[i]);
			}

			BufferedReader br3 = new BufferedReader(new FileReader(UNIGRAM));
			String line3 = null;
			HashMap<String, String> qtermsIList = new HashMap<>();
			while((line3 = br3.readLine()) != null){
				String[] splits = line3.split("\\s");
				String term = splits[0].trim();
				if(queryTerms.contains(term)){
					String list = splits[2];
					qtermsIList.put(term, list);
				}
			}
			br3.close();

			HashMap<String, List<QueryTermFrequency>> documentWithQuery = new HashMap<>();
			for(Map.Entry<String, String> entry:qtermsIList.entrySet()){
				String qterm = entry.getKey();
				int len = entry.getValue().length();
					String documents = entry.getValue().substring(1, len-2);
					String[] docIds = documents.split(",");
					List<QueryTermFrequency> documentsList = new ArrayList<>();
					for(String s:docIds){
						String substring = s.substring(1, s.length()-1);
						String[] word = substring.split(DELIMITER);
							String documentTitle = word[0];
							int term_frequency = Integer.parseInt(word[1]);
							QueryTermFrequency qtf = new QueryTermFrequency(qterm, term_frequency);
							if(documentWithQuery.containsKey(documentTitle)){
								List<QueryTermFrequency> existing_list = documentWithQuery.get(documentTitle);
								existing_list.add(qtf);
								documentWithQuery.put(documentTitle,existing_list);
							}else{
								List<QueryTermFrequency> new_list = new ArrayList<>();
								new_list.add(qtf);
								documentWithQuery.put(documentTitle,new_list);
							}
					}
			}

			// TFIDF Calculation
			for(Map.Entry<String, List<QueryTermFrequency>> entry:documentWithQuery.entrySet()){
				List<QueryTermFrequency> val = entry.getValue();
				// Display the List
				double final_tfidf_value = 0.0;
				for(QueryTermFrequency qtf:val){
					double tf = Math.log(1+qtf.termFrequency);
					double idf = Math.log((double)N/(1+fileCountforTerm.get(qtf.queryTerm)));
					final_tfidf_value += tf*idf;
				}
				tfidf.put(entry.getKey(), final_tfidf_value);
			}



			List<Map.Entry<String, Double>> entries = new ArrayList<Map.Entry<String, Double>>(tfidf.entrySet());
			Collections.sort(entries, new Comparator<Map.Entry<String, Double>>() {
					public int compare(
							Map.Entry<String, Double> entry1, Map.Entry<String, Double> entry2) {
						return entry2.getValue().compareTo(entry1.getValue());
					}
			});

			if(entries.size() > 0){
				String fileName = "TFIDF Output for Q"+queryId+".txt";
				File file = new File(System.getProperty("user.dir")+"/TFIDF Output/"+fileName);
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
				int count = 1;
				for(Map.Entry<String, Double> val:entries){
					if(count >= 101){
						break;
					}
					StringBuffer sb = new StringBuffer("");
					sb.append(queryId+" ");
					sb.append("Q0 ");
					sb.append(val.getKey()+" ");
					sb.append(count + " ");
					sb.append(val.getValue() + " ");
					sb.append(SYSTEM_NAME + " ");
					fileWriter.write(sb.toString());
					fileWriter.write("\r\n");
					count++;
				}
				fileWriter.flush();
				fileWriter.close();
			}
		}
		br.close();
		System.out.println("Done with TFIDF");









  }


}
