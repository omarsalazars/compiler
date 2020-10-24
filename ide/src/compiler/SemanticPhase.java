package compiler;

public class SemanticPhase extends CompilerPhase{
    public SemanticPhase(String path){
        super(path);
    }

    public SemanticPhase(){
        super(System.getProperty("user.dir")+"/../semantic.py");
    }
}
