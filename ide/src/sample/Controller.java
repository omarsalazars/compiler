package sample;

import compiler.AST;
import compiler.Compiler;
import filemanager.FileManager;
import javafx.application.Platform;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import org.fxmisc.richtext.CodeArea;
import org.fxmisc.richtext.LineNumberFactory;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Controller {

    @FXML
    CodeArea editor;
    @FXML
    Button compile, lexic, syntactic, semantic, addFile, saveButton, openButton;
    @FXML
    TextArea lexicOutput;
    @FXML
    TreeView parserOutput;
    @FXML
    TabPane filesTabs;
    @FXML
    AnchorPane anchorPane;
    @FXML
    GridPane mainPane;

    private FileManager fileManager;
    private Compiler COMPILER;
    private SyntaxHighlighter HIGHLIGHTER;

    @FXML
    public void initialize(){
        filesTabs.setTabClosingPolicy(TabPane.TabClosingPolicy.SELECTED_TAB);
        fileManager = new FileManager();
        lexicOutput.setEditable(false);
        COMPILER = new Compiler();
        HIGHLIGHTER = new SyntaxHighlighter(editor);
        setHighlighter();

        compile.setOnAction(actionEvent -> {
            fileManager.getCurrent().save(mainPane.getScene().getWindow());
            COMPILER.Compile(fileManager.getCurrent().getFile().getAbsolutePath());
        });

        lexic.setOnAction( actionEvent -> {
            fileManager.getCurrent().setContent(editor.getText());
            if(fileManager.getCurrent().save(mainPane.getScene().getWindow())) {
                lexicOutput.setText(COMPILER.getLexer().run(fileManager.getCurrent().getFile().getAbsolutePath()));
            }else{
                System.out.println("Not saved");
            }
        });

        syntactic.setOnAction( actionEvent -> {
            fileManager.getCurrent().setContent(editor.getText());
            if(fileManager.getCurrent().save(mainPane.getScene().getWindow())) {
                AST ast = new AST(COMPILER.getParser().run(fileManager.getCurrent().getFile().getAbsolutePath()));
                parserOutput.setRoot(ast.toTreeNode());
            }else{
                System.out.println("Not saved");
            }
        });
        semantic.setOnAction( actionEvent -> COMPILER.getSemantic().run(fileManager.getCurrent().getFile().getAbsolutePath()) );

        fileManager.newFile();
        filesTabs.getTabs().add(fileManager.getCurrent().getTab());
        filesTabs.getSelectionModel().select(fileManager.getCurrent().getTab());
        fileManager.getCurrent().getTab().setContent(editor);

        //Files
        filesTabs.getSelectionModel().selectedItemProperty().addListener(
                new ChangeListener<Tab>() {
                    @Override
                    public void changed(ObservableValue<? extends Tab> observable, Tab oldValue, Tab newValue) {
                        if(oldValue != null)
                            oldValue.setContent(null);
                        fileManager.getCurrent().setContent(editor.getText());
                        fileManager.setCurrent(newValue);
                        editor.replaceText(0,editor.getText().length(),fileManager.getCurrent().getContent());
                        fileManager.getCurrent().getTab().setContent(editor);
                    }
                }
        );
        filesTabs.getTabs().forEach(tab -> {
            tab.setOnClosed(e -> {
                fileManager.remove(tab);
            });
        });
        addFile.setOnAction(e -> {
            fileManager.getCurrent().setContent(editor.getText());
            fileManager.newFile();
            filesTabs.getTabs().add(fileManager.getCurrent().getTab());
            editor.replaceText(0,editor.getText().length(),"");
            filesTabs.getSelectionModel().select(fileManager.getCurrent().getTab());
        });

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