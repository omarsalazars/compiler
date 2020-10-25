package filemanager;

import javafx.scene.control.Tab;
import java.util.ArrayList;

public class FileManager {

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

}
