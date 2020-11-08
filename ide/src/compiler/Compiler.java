package compiler;

public class Compiler {

    private LexicalPhase lex;
    private SyntacticPhase parser;
    private SemanticPhase semantic;
    private String projectPath;

    public Compiler(){
        /* /home/omar/Documents/compiler/ide */
        projectPath = System.getProperty("user.dir");
        lex = new LexicalPhase();
        parser = new SyntacticPhase();
        semantic = new SemanticPhase();
    }

    public LexicalPhase getLexer() {
        return lex;
    }

    public SyntacticPhase getParser() {
        return parser;
    }

    public SemanticPhase getSemantic() {
        return semantic;
    }

    public Boolean Compile(String filePath){
        try {
            this.lex.run(filePath);
            this.parser.run(filePath);
            return true;
        }catch(Exception e){
            return false;
        }
    }
}
