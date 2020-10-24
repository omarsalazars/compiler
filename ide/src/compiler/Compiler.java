package compiler;

public class Compiler {

    private LexicalPhase lex;
    private SyntacticPhase parser;

    public LexicalPhase getLexer() {
        return lex;
    }

    public SyntacticPhase getParser() {
        return parser;
    }

    public SemanticPhase getSemantic() {
        return semantic;
    }

    private SemanticPhase semantic;
    private String projectPath;

    public Compiler(){
        /* /home/omar/Documents/compiler/ide */
        projectPath = System.getProperty("user.dir");
        lex = new LexicalPhase();
        parser = new SyntacticPhase();
    }

    public Boolean Compile(String code){
        try {
            this.lex.run(code);
            this.parser.run(code);
            return true;
        }catch(Exception e){
            return false;
        }
    }
}
