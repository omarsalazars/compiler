package sample;

import compiler.AST;
import compiler.Compiler;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TreeView;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import org.fxmisc.richtext.CodeArea;
import org.fxmisc.richtext.LineNumberFactory;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Controller {

    @FXML
    CodeArea editor;
    @FXML
    Button compile, lexic, syntactic, semantic;
    @FXML
    TextArea lexicOutput;
    @FXML
    TreeView parserOutput;

    private Compiler COMPILER;
    private SyntaxHighlighter HIGHLIGHTER;
    private String filePath;

    @FXML
    public void initialize(){
        COMPILER = new Compiler();
        HIGHLIGHTER = new SyntaxHighlighter(editor);
        setHighlighter();

        filePath = System.getProperty("user.dir")+"/../a";

        compile.setOnAction(actionEvent -> COMPILER.Compile(editor.getText()));
        lexic.setOnAction( actionEvent -> lexicOutput.setText(COMPILER.getLexer().run(filePath)));
        syntactic.setOnAction( actionEvent -> {
            AST ast = new AST(COMPILER.getParser().run(filePath));
            parserOutput.setRoot(ast.toTreeNode());
        });
        semantic.setOnAction( actionEvent -> COMPILER.getSemantic().run(filePath) );
    }

    private void setHighlighter(){
        editor.setParagraphGraphicFactory(LineNumberFactory.get(editor));
        editor.getVisibleParagraphs().addModificationObserver(
                HIGHLIGHTER.getSyntaxStyler()
        );

        final Pattern whitespace = Pattern.compile("^\\s+");
        editor.addEventHandler(KeyEvent.KEY_PRESSED, KE -> {
            if(KE.getCode() == KeyCode.ENTER){
                int caretPosition = editor.getCaretPosition();
                int currentParagraph = editor.getCurrentParagraph();
                Matcher m0 = whitespace.matcher( editor.getParagraph( currentParagraph-1 ).getSegments().get(0));
                if(m0.find()) Platform.runLater( () -> editor.insertText(caretPosition, m0.group()) );
            }
        } );
    }
}