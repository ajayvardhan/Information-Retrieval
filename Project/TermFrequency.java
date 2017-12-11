public class TermFrequency{

  protected String DOC_TITLE;
  protected int TF;


  public TermFrequency(){
    this.DOC_TITLE = null;
    this.TF = 0;
  }


  public void setTermFrequency(String DOC_TITLE, int TF){
    this.DOC_TITLE = DOC_TITLE;
    this.TF = TF;
  }



}
