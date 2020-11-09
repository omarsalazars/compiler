package compiler;

public class SyntacticPhase extends CompilerPhase{

    public String outPath;

    public SyntacticPhase(String path){
        super(path);
        outPath = System.getProperty("user.dir")+"/../out/parse";
    }

    public SyntacticPhase(){
        super(System.getProperty("user.dir")+"/../parser.py");
        outPath = System.getProperty("user.dir")+"/../out/parse";
    }
}
