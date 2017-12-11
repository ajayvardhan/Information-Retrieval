import java.io.File;
import org.jsoup.Connection;
import org.jsoup.HttpStatusException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.IOException;
import java.util.List;
import java.util.ArrayList;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Map;
import java.util.HashMap;

public class TextProcessing{

  private static String DOCUMENTS = "Documents/cacm";
  private static String QUERY_DOCUMENT = "cacm.query.txt";


  private static void processFiles() throws IOException{

    File folder = new File(DOCUMENTS);
    File[] listOfFiles = folder.listFiles();

    for (File file : listOfFiles) {
        if (file.isFile()) {
          Document doc = Jsoup.parse(file, "UTF-8");
          String doc_content = doc.select("pre").text(); //Extract pre tag content
          String processed_text = processText(doc_content);
          writeToFile(processed_text, file.getName());
        }
    }
  }

  private static void processQuery() throws IOException{

    File qFile = new File(QUERY_DOCUMENT);
    Map<Integer, String> querywithId = new HashMap<>();
    boolean queryFound = false;
    if (qFile.isFile()) {
      BufferedReader br = new BufferedReader(new FileReader(qFile));
      String li = null;
      String queryId = null;
      String queryContent = "";
	    while((li = br.readLine()) != null){
        if(li.equals("<DOC>")){
          queryFound = true;
          continue;
        }
        if(li.equals("</DOC>")){
          queryFound = false;
          querywithId.put(Integer.parseInt(queryId), queryContent);
          queryContent = "";
        }
        if(queryFound){
            if(li.contains("<DOCNO>")){
              String[] split = li.split("\\s");
              queryId = split[1].trim();
            }else if(li.trim().length()>0){
              queryContent += li.replace("\n"," ").trim() + " ";
            }
        }
      }
    }


    writeToQueryFile(querywithId);


  }



  private static String processText(String text){
      return punctuation(case_folding(text));
  }

  private static String case_folding(String text){

    text = text.replaceAll("\n"," ");
    text = text.replaceAll("\t"," ");
    text = text.trim().replaceAll("\\s{2,}", " ");
    String[] words = text.split(" ");
    StringBuilder str = new StringBuilder("");
    String startingWithAlphabets = "^[a-zA-Z0-9]";
    // Create a Pattern object
    Pattern r = Pattern.compile(startingWithAlphabets);
    int count = 0;
    for(String w:words){
      Matcher m = r.matcher(w);
      if(m.find()){
        str.append(w.toLowerCase());
        str.append(" ");
        count++;
      }
    }
    return str.toString();
  }

  private static String punctuation(String text){
      StringBuilder str = new StringBuilder("");
      String[] words = text.split(" ");
      String reg = "^[:.,]";
      String regExp3 = "[.,:;?]+$";
      String regExp = "^[a-zA-Z0-9]";
      String endsWith = "[\")]+$";
      Pattern p = Pattern.compile(reg);
      Pattern q = Pattern.compile(regExp3);
      Pattern r = Pattern.compile(regExp);
      Pattern s = Pattern.compile(endsWith);
      int count = 0;
      for(String w:words){
        Matcher n = q.matcher(w);
        Matcher o = r.matcher(w);
        Matcher m = p.matcher(w);
        Matcher z = s.matcher(w);
        if(!m.find()){
          String strippedInput = w;
          if(n.find() && o.find()){
            strippedInput = w.replaceAll("\\W", " ");
          }
          else if(z.find() || w.endsWith("\"")){
            strippedInput = w.substring(0, w.length()-1);
          }
          if(strippedInput.indexOf(",") != -1){
            strippedInput = strippedInput.replace(",", " ");
          }
          if(strippedInput.indexOf(".") != -1){
            strippedInput = strippedInput.replace(".", " ");
          }
          strippedInput = strippedInput.trim().replaceAll("\\s{2,}", " ");
          str.append(strippedInput);
          str.append(" ");
        }
      }
  return str.toString();
}

  private static void writeToFile(String processed_text, String fileName)
  throws IOException{
    List<String> words = splitWords(processed_text);

    File file = new File(System.getProperty("user.dir")+"/Processed/"+fileName+".txt");
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
    for(String w:words){
			fileWriter.write(w.trim());
			fileWriter.write(" ");
		}
    fileWriter.flush();
		fileWriter.close();
  }

  private static void writeToQueryFile(Map<Integer, String> map)
  throws IOException{
    File file = new File(System.getProperty("user.dir")+"/Processed Query/Query.txt");
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
    for(Map.Entry<Integer, String> entry:map.entrySet()){
      String queryId = entry.getKey().toString();
      String afterProcess = processText(entry.getValue());
      afterProcess.trim().replaceAll("\\s{2,}", " ");
      fileWriter.write(queryId.trim() + " " +afterProcess.trim());
      fileWriter.write("\n");
    }
    fileWriter.flush();
		fileWriter.close();
  }


  private static List<String> splitWords(String text){
    String[] words = text.split(" ");
    List<String> word = new ArrayList<>();
    for(String w:words){
      word.add(w);
    }
    return word;
  }





  public static void main(String args[]) throws IOException{
      processFiles();
      processQuery();
  }





}
