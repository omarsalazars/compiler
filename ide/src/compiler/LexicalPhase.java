package compiler;

public class LexicalPhase extends CompilerPhase {

    public String outPath;

    public LexicalPhase(String path){
        super(path);
        outPath = System.getProperty("user.dir")+"/../out/tokens";
    }

    public LexicalPhase(){
        super(System.getProperty("user.dir")+"/../lex.py");
        outPath = System.getProperty("user.dir")+"/../out/tokens";
    }
}
