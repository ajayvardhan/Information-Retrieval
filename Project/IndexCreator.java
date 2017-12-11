import java.util.Scanner;
import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.TreeMap;
import java.io.LineNumberReader;
import java.util.Collections;
import java.util.Set;
import java.util.Map.Entry;
import java.util.Comparator;


public class IndexCreator{

  private static Map<String, List<TermFrequency>> unigrams = new TreeMap<>();
  private static Map<String, Integer> filecount = new HashMap<>();
  private static HashMap<Integer, String> document_id = new HashMap<>();
  private static HashMap<String, Integer>  ni = new HashMap<>();
  private static String UNIGRAM_FILENAME = "Unigram";
  private static HashMap<String, Integer> wordCountInCollection = new HashMap<>();
  private static String STOPPED_CORPUS = "/Stopped Corpus/";
  private static String WITHOUT_STOPPING = "/Processed/";
  private static String STEMMED_CORPUS = "/Stemmed/";
  private static String CORPUS_SELECTED = WITHOUT_STOPPING; //Default

  // Inverted Index Creation
  private static File[] readFiles(){
    File folder = new File(System.getProperty("user.dir")+CORPUS_SELECTED);
    File[] list = folder.listFiles();
    return list;
  }

  private static void unigrams() throws FileNotFoundException, IOException{


       unigrams = new TreeMap<>();
       File[] listofFiles = readFiles();
       for(File f:listofFiles){
         if(f.isFile()){
           BufferedReader br = new BufferedReader(new FileReader(f));
           String line = null;
           line = br.readLine(); //Read the doc id
           br.close();
           String[] split = line.split(" ");
           filecount.put(f.getName(), split.length);
           Map<String, Integer> word_count = new HashMap<>();
           for(int i=1;i<split.length;i++){
             word_count.put(split[i], word_count.getOrDefault(split[i],0) + 1);
           }
           // Now create inverted index
           for(Map.Entry<String, Integer> entry:word_count.entrySet()){
                String word = entry.getKey();
                int tf = entry.getValue();
                TermFrequency t = new TermFrequency();
                t.setTermFrequency(f.getName(), tf);
                if(unigrams.containsKey(word)){
                  List<TermFrequency> existing_list = unigrams.get(word);
                  existing_list.add(t);
                  unigrams.put(word, existing_list);
                }else{
                  List<TermFrequency> list = new ArrayList<>();
                  list.add(t);
                  unigrams.put(word, list);
                }
           }
         }
       }
  }

  private static void writeFile(String fileName,
                                Map<String, List<TermFrequency>> grams)
  throws IOException{

    File file = new File(System.getProperty("user.dir")+"/Inverted Indexes/" +fileName);
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
    for(Map.Entry<String, List<TermFrequency>> entry:grams.entrySet()){
      String term = entry.getKey();
      fileWriter.write(term + " --> ");
      int count = 0;
      List<TermFrequency> tfList = entry.getValue();
      ni.put(term, tfList.size());
      fileWriter.write("[");
      for(TermFrequency t:tfList){
        fileWriter.write("("+t.DOC_TITLE+"##"+t.TF+")");
        fileWriter.write(",");
        count += t.TF;
      }
      wordCountInCollection.put(entry.getKey(),count);
      fileWriter.write("]");
      fileWriter.write("\r\n");

    }
    fileWriter.flush();
		fileWriter.close();
  }

  private static void writeDocCount(String fileName) throws IOException{

    int totalcount = 0;
    File file = new File(System.getProperty("user.dir")+"/File Size/" +fileName);
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
    for(Map.Entry<String, Integer> entry:filecount.entrySet()){
      int count = entry.getValue();
      totalcount += entry.getValue();
      fileWriter.write(entry.getKey() + " " +count);
      fileWriter.write("\r\n");
    }
    fileWriter.write("1111" + " " +totalcount);
    fileWriter.write("\r\n");
    fileWriter.flush();
    fileWriter.close();
  }


  private static void writeNI(String fileName) throws IOException{

    File file = new File(System.getProperty("user.dir")+"/File Size/" +fileName);
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
    for(Map.Entry<String, Integer> entry:ni.entrySet()){
      int count = entry.getValue();
      fileWriter.write(entry.getKey() + " " +count);
      fileWriter.write("\r\n");
    }
    fileWriter.flush();
    fileWriter.close();
  }

  private static void writeWordCountInCollection(String fileName) throws IOException{

    File file = new File(System.getProperty("user.dir")+"/File Size/" +fileName);
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
    for(Map.Entry<String, Integer> entry: wordCountInCollection.entrySet()){
      String word = entry.getKey();
      fileWriter.write(word + " " + entry.getValue());
      fileWriter.write("\r\n");
    }
    fileWriter.flush();
    fileWriter.close();


  }




  public static void main(String args[]) throws FileNotFoundException, IOException {

      String corpus = args[0];
      if(corpus.equals("Stemmed")){
        CORPUS_SELECTED = STEMMED_CORPUS;
      }else if(corpus.equals("Stopped")){
        CORPUS_SELECTED = STOPPED_CORPUS;
      }

      unigrams();
      writeDocCount("NoDocWordOccurs");
      writeFile(UNIGRAM_FILENAME, unigrams);
      writeNI("NI");
      writeWordCountInCollection("WordCountInCollection");
  }


}
