package filemanager;

import compiler.AST;
import javafx.scene.control.Tab;
import javafx.stage.FileChooser;
import javafx.stage.Window;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

public class FileEditor{

    private String name;
    private Tab tab;
    private File file;
    private String content;
    private AST parser;
    private String lexerOutput;

    public FileEditor(String name) {
        this.content = "";
        this.name = name;
        tab = new Tab(name);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
        this.tab.setText(this.name);
    }

    public Tab getTab() {
        return tab;
    }

    public void setTab(Tab tab) {
        this.tab = tab;
    }

    public File getFile() {
        return file;
    }

    public void setFile(File file) {
        this.file = file;
    }

    public String getContent(){
        return this.content;
    }

    public void setContent(String content){
        this.content = content;
    }

    public Boolean save(Window window){
        if(!this.isSaved()){
            //Save with filechooser
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Guardar Archivo");
            this.file = fileChooser.showSaveDialog(window);
        }
        if(this.file == null) return false;
        this.tab.setText(this.file.getName());
        return this.writeToFile();
    }

    public Boolean isSaved(){
        return this.file != null;
    }

    private Boolean writeToFile(){
        try {
            PrintWriter printWriter = new PrintWriter(this.file);
            printWriter.println(this.content);
            printWriter.close();
        }catch(IOException e){
            e.printStackTrace();
            return false;
        }
        return true;
    }
}
