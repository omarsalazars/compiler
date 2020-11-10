package compiler;

public class SemanticPhase extends CompilerPhase{

    public String outPath;
    public String symTableOut;

    public SemanticPhase(String path){
        super(path);
        outPath = System.getProperty("user.dir")+"/out/ast";
        symTableOut = System.getProperty("user.dir")+"/out/sym";
    }

    public SemanticPhase(){
        super(System.getProperty("user.dir")+"/../semantic.py");
        outPath = System.getProperty("user.dir")+"/out/ast";
        symTableOut = System.getProperty("user.dir")+"/out/sym";
    }
}
