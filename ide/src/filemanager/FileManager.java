package filemanager;

import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.stage.FileChooser;
import javafx.stage.Window;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class FileManager{

    private ArrayList<FileEditor> files;
    private Integer untitledCount = 0;
    private Integer current = 0;

    public FileManager(){
        files = new ArrayList<>();
    }

    public void newFile(){
        untitledCount++;
        files.add(new FileEditor("Untitled "+untitledCount));
        current = files.size()-1;
    }

    public void remove(Tab tab){
        FileEditor index = null;
        for (FileEditor file : files) {
            if(file.getTab().equals(tab)){
                index = file;
            }
        }
        files.remove(index);
    }

    public FileEditor getCurrent(){
        return files.get(current);
    }

    public void setCurrent(Integer current){
        this.current = current;
    }

    public void setCurrent(FileEditor file){
        this.current = files.indexOf(file);
    }

    public void setCurrent(Tab tab){
        FileEditor index = null;
        for (FileEditor file : files) {
            if(file.getTab().equals(tab)){
                index = file;
            }
        }

        this.current = files.indexOf(index) != -1 ? files.indexOf(index) : this.current;
    }

    public ArrayList<FileEditor> getFiles(){
        return this.files;
    }

    public FileEditor find(Tab tab){
        FileEditor index = null;
        for (FileEditor file : files) {
            if(file.getTab().equals(tab)){
                index = file;
            }
        }
        return index;
    }

    public Boolean openFile(Window window){
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Abrir archivo");
        File file = fileChooser.showOpenDialog(window);
        if(file != null){
            try {
                for (FileEditor it : files) {
                    if(it.getFile() == null) continue;
                    if (it.getFile().getAbsolutePath().equals(file.getAbsolutePath()))
                        throw new Exception("File already opened");
                }
            }catch(Exception e){
                e.printStackTrace();
                return false;
            }
            FileEditor fe = new FileEditor(file.getName());
            fe.setFile(file);
            fe.setContent(this.getFileContents(file));
            files.add(fe);
            this.current = files.size()-1;
        }
        return file != null;
    }

    public void saveRecents(){
        FileWriter writer = null;
        try{
            File f = new File("recents.txt");
            f.createNewFile();
            writer = new FileWriter(f);
            for(FileEditor fileEditor : this.files){
                if(fileEditor.getFile()!=null) {
                    writer.write(fileEditor.getFile().getAbsolutePath()+"\n");
                }
            }
        }catch(IOException e){
            e.printStackTrace();
        }finally {
            try{
                writer.close();
            }catch (IOException e){
                e.printStackTrace();
            }
        }
    }

    public void loadRecents(TabPane tabPane){
        Scanner scanner = null;
        try{
            File f = new File("recents.txt");
            scanner = new Scanner(f);
            while(scanner.hasNextLine()){
                String path = scanner.nextLine();
                File cf = new File(path);
                if(!cf.exists()) continue;
                FileEditor fe = new FileEditor("");
                fe.setFile(cf);
                fe.setName(fe.getFile().getName());
                fe.setContent(this.getFileContents(fe.getFile()));
                files.add(fe);
                tabPane.getTabs().add(fe.getTab());
                this.current = files.size()-1;
                tabPane.getSelectionModel().select(fe.getTab());
            }
        }catch (FileNotFoundException e){
            e.printStackTrace();
        }
    }

    private String getFileContents(File f){
        Scanner scanner = null;
        String content = "";
        try{
            scanner = new Scanner(f);
            while(scanner.hasNextLine()){
                content += scanner.nextLine();
                if(scanner.hasNextLine()){
                    content += "\n";
                }
            }
        }catch (FileNotFoundException e){
            e.printStackTrace();
        }
        return content;
    }
}
