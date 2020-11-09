package compiler;

import java.io.*;
import java.util.Scanner;

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

    public String readOutput(String filepath){
        Scanner scanner = null;
        String content = "";
        File f = new File(filepath);
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

    private String executeProcess(String programPath, String filePath){
        String s = "", line;
        try {
            Process p = Runtime.getRuntime().exec("python "+programPath+" "+filePath);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
            BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
            while ((line = stdInput.readLine()) != null) {
                s += line+"\n";
            }
            while( (line = stdError.readLine()) != null){
                s += line+"\n";
            }
        }catch(IOException e){
            e.printStackTrace();
        }
        return s;
    }
}
