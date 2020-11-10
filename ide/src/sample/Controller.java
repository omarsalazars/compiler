package sample;

import compiler.AST;
import compiler.Compiler;
import filemanager.FileManager;
import javafx.application.Platform;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.GridPane;
import org.fxmisc.richtext.CodeArea;
import org.fxmisc.richtext.LineNumberFactory;
import org.json.JSONObject;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Controller {

    @FXML
    CodeArea editor;
    @FXML
    Button compile, lexic, syntactic, semantic, addFile, saveButton, openButton;
    @FXML
    TextArea lexicOutput, console;
    @FXML
    TreeView parserOutput, semanticOutput;
    @FXML
    TabPane filesTabs;
    @FXML
    AnchorPane anchorPane;
    @FXML
    GridPane mainPane;
    @FXML
    TableView<Var> symTable;
    @FXML
    TableColumn nameCol, typeCol, locCol, valCol, lineCol;

    private FileManager fileManager = new FileManager();
    private Compiler COMPILER = new Compiler();
    private SyntaxHighlighter HIGHLIGHTER;

    @FXML
    public void initialize(){
        HIGHLIGHTER = new SyntaxHighlighter(editor);
        filesTabs.setTabClosingPolicy(TabPane.TabClosingPolicy.SELECTED_TAB);
        fileManager.loadRecents(filesTabs);
        if(fileManager.getFiles().size() == 0) {
            fileManager.newFile();
            filesTabs.getTabs().add(fileManager.getCurrent().getTab());
            filesTabs.getSelectionModel().select(fileManager.getCurrent().getTab());
        }
        editor.replaceText(0,editor.getText().length(),fileManager.getCurrent().getContent());
        fileManager.getCurrent().getTab().setContent(editor);

        lexicOutput.setEditable(false);
        setHighlighter();
        setTableView();

        openButton.setOnAction(AE -> this.openButtonAction(AE));
        saveButton.setOnAction(AE -> this.saveButtonAction(AE));

        compile.setOnAction(actionEvent -> {
            Alert a = new Alert(Alert.AlertType.ERROR);
            a.setContentText("Acción no implementada");
            a.show();
        });

        lexic.setOnAction( actionEvent -> lexicAction(actionEvent));
        syntactic.setOnAction( actionEvent -> syntacticAction(actionEvent));
        semantic.setOnAction( actionEvent -> semanticAction(actionEvent));

        //Files
        filesTabs.getSelectionModel().selectedItemProperty().addListener(
                new ChangeListener<Tab>() {
                    @Override
                    public void changed(ObservableValue<? extends Tab> observable, Tab oldValue, Tab newValue) {
                        changeTabAction(oldValue, newValue);
                    }
                }
        );

        filesTabs.getTabs().forEach(tab -> {
            tab.setOnClosed(e -> {
                fileManager.remove(tab);
            });
        });

        addFile.setOnAction(AE -> this.addFileAction(AE));
    }

    public void addFileAction(ActionEvent AE){
        fileManager.newFile();
        filesTabs.getTabs().add(fileManager.getCurrent().getTab());
        editor.replaceText(0,editor.getText().length(),"");
        filesTabs.getSelectionModel().select(fileManager.getCurrent().getTab());
    }

    public void changeTabAction(Tab oldValue, Tab newValue){
        if(oldValue != null)
            oldValue.setContent(null);
        fileManager.getCurrent().setContent(editor.getText());
        fileManager.setCurrent(newValue);
        editor.replaceText(0,editor.getText().length(),fileManager.getCurrent().getContent());
        fileManager.getCurrent().getTab().setContent(editor);

        //Outputs
        lexicOutput.setText(fileManager.getCurrent().getLexerOutput());
        if(fileManager.getCurrent().getParser() != null)
            parserOutput.setRoot(fileManager.getCurrent().getParser().toTreeNode());
        else
            parserOutput.setRoot(null);
    }

    public Boolean lexicAction(ActionEvent AE){
        fileManager.getCurrent().setContent(editor.getText());
        if(fileManager.getCurrent().save(mainPane.getScene().getWindow())) {
            String output = COMPILER.getLexer().run(fileManager.getCurrent().getFile().getAbsolutePath());
            int errorIndex = output.indexOf("lexer.LexerError");
            if(errorIndex != -1){
                console.appendText(output.substring(errorIndex));
                fileManager.getCurrent().setLexerOutput("");
                lexicOutput.setText("Error.");
                console.setStyle("-fx-text-fill: red ;");
            }else {
                console.setStyle("-fx-text-fill: black ;");
                String tokens = COMPILER.getLexer().readOutput(COMPILER.getLexer().outPath);
                fileManager.getCurrent().setLexerOutput(tokens);
                lexicOutput.setText(tokens);
                console.appendText("Lexic analyzer successfully executed.\n");
                return true;
            }
        }else{
            System.out.println("Not saved");
        }
        return false;
    }

    public Boolean syntacticAction(ActionEvent AE){
        if(!this.lexicAction(AE)) return false;
        fileManager.getCurrent().setContent(editor.getText());
        if(fileManager.getCurrent().save(mainPane.getScene().getWindow())) {
            String output = COMPILER.getParser().run(fileManager.getCurrent().getFile().getAbsolutePath());
            int errorIndex = output.indexOf("parser.ParseError.ParseError");
            if(errorIndex != -1){
                console.appendText(output.substring(errorIndex));
                fileManager.getCurrent().setParser(null);
                parserOutput.setRoot(null);
                console.setStyle("-fx-text-fill: red ;");
            }else {
                console.setStyle("-fx-text-fill: black ;");
                String json = COMPILER.getSemantic().readOutput(COMPILER.getSemantic().outPath);
                AST ast = new AST(json);
                fileManager.getCurrent().setParser(ast);
                parserOutput.setRoot(ast.toTreeNode());
                console.appendText("Syntactic analyzer successfully executed.\n");
                return true;
            }
        }else{
            System.out.println("Not saved");
        }
        return false;
    }

    public Boolean semanticAction(ActionEvent AE){
        if(!this.syntacticAction(AE)) return false;
        fileManager.getCurrent().setContent(editor.getText());
        if(fileManager.getCurrent().save(mainPane.getScene().getWindow())) {
            String output = COMPILER.getSemantic().run(fileManager.getCurrent().getFile().getAbsolutePath());
            int errorIndex = output.indexOf("semantic.SemanticError.SemanticError");
            if(errorIndex != -1){
                console.appendText(output.substring(errorIndex));
                fileManager.getCurrent().setSemantic(null);
                semanticOutput.setRoot(null);
                console.setStyle("-fx-text-fill: red ;");
            }else {
                console.setStyle("-fx-text-fill: black ;");
                console.appendText(output);
                //AST
                String json = COMPILER.getSemantic().readOutput(COMPILER.getSemantic().outPath);
                AST ast = new AST(json);
                fileManager.getCurrent().setSemantic(ast);
                semanticOutput.setRoot(ast.toTreeNode());

                //SymTable
                json = COMPILER.getSemantic().readOutput(COMPILER.getSemantic().symTableOut);
                symTable.setItems(Var.jsonToList(new JSONObject(json)));
                console.appendText("Semantic analyzer successfully executed.\n");
                return true;
            }
        }else{
            System.out.println("Not saved");
        }
        return false;
    }

    public void openButtonAction(ActionEvent AE){
        if(fileManager.openFile(mainPane.getScene().getWindow())) {
            filesTabs.getTabs().add(fileManager.getCurrent().getTab());
            fileManager.getCurrent().getTab().setContent(editor);
            editor.replaceText(0, editor.getText().length(), fileManager.getCurrent().getContent());
            filesTabs.getSelectionModel().select(fileManager.getCurrent().getTab());
        }else{
            Alert a = new Alert(Alert.AlertType.ERROR);
            a.setContentText("Error abriendo el archivo.");
            a.show();
        }
    }

    public void saveButtonAction(ActionEvent AE){
        Alert a = new Alert(Alert.AlertType.ERROR);
        a.setContentText("Action not implemented yet.");
        a.show();
    }

    public void shutdown(){
        fileManager.saveRecents();
        Platform.exit();
    }

    private void setTableView(){
        nameCol.setCellValueFactory(
                new PropertyValueFactory<Var, String>("name")
        );
        typeCol.setCellValueFactory(
                new PropertyValueFactory<Var, String>("type")
        );
        locCol.setCellValueFactory(
                new PropertyValueFactory<Var, Integer>("loc")
        );
        lineCol.setCellValueFactory(
                new PropertyValueFactory<Var, String>("lines")
        );
        /*
        valCol.setCellFactory(
                new PropertyValueFactory<Var, String>("val")
        );
         */
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