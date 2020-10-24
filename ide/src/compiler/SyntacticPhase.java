package compiler;

public class SyntacticPhase extends CompilerPhase{
    public SyntacticPhase(String path){
        super(path);
    }

    public SyntacticPhase(){
        super(System.getProperty("user.dir")+"/../parser.py");
    }
}
