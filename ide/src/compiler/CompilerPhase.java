package compiler;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public abstract class CompilerPhase {

    private String path;

    public CompilerPhase(){ }

    public CompilerPhase(String path){
        this.setPath(path);
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path){
        this.path = path;
    }

    public String run(String filePath){
        return this.executeProcess(this.path, filePath);
    }

    private String executeProcess(String programPath, String filePath){
        String s = "", line;
        try {
            System.out.println(filePath);
            Process p = Runtime.getRuntime().exec("python "+programPath+" "+filePath);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            //BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            while ((line = stdInput.readLine()) != null) {
                s += line+"\n";
            }
        }catch(IOException e){
            e.printStackTrace();
        }
        return s;
    }
}
