package sample;

public class Compiler {

    private String lexicAnalyzer;
    private String syntacticAnalyzer;
    private String semanticAnalyzer;

    public Compiler(){

    }

    public void Lexic(String code){
    }

    public void Syntactic(String code){

    }

    public void Semantic(String code){

    }

    public Boolean Compile(String code){
        try {
            this.Lexic(code);
            this.Syntactic(code);
            this.Semantic(code);
            return true;
        }catch(Exception e){
            return false;
        }
    }
}
