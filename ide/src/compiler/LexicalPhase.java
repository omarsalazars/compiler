package compiler;

public class LexicalPhase extends CompilerPhase {
    public LexicalPhase(String path){
        super(path);
    }

    public LexicalPhase(){
        super(System.getProperty("user.dir")+"/../lex.py");
    }
}
