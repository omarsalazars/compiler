package sample;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
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

    private Compiler COMPILER;
    private SyntaxHighlighter HIGHLIGHTER;

    @FXML
    public void initialize(){
        COMPILER = new Compiler();
        HIGHLIGHTER = new SyntaxHighlighter(editor);
        setHighlighter();

        compile.setOnAction(actionEvent -> COMPILER.Compile(editor.getText()));
        lexic.setOnAction( actionEvent -> COMPILER.Lexic(editor.getText()) );
        syntactic.setOnAction( actionEvent -> COMPILER.Syntactic(editor.getText()) );
        semantic.setOnAction( actionEvent -> COMPILER.Semantic(editor.getText()) );
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