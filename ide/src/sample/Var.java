package sample;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Var {
    String name;
    String type;
    Integer loc;
    String lines;
    Object val;

    static ObservableList<Var> jsonToList(JSONObject json){
        Iterator<String> it = json.keys();
        ArrayList<Var> varList = new ArrayList<>();
        while(it.hasNext()){
            String key = it.next();
            if(key.equals("loc")) continue;
            JSONObject currentObject = json.getJSONObject(key);
            Iterator<String> it2 = currentObject.keys();
            Var var = new Var();
            var.name = key;
            while(it2.hasNext()){
                String k = it2.next();
                switch (k){
                    case "type":
                        JSONObject type = currentObject.getJSONObject(k);
                        JSONObject token = type.getJSONObject("token");
                        var.type = token.getString("type");
                        break;
                    case "val":
                        Object val = currentObject.get(k);
                        var.val = val;
                        if(val instanceof Boolean){
                            Boolean v = (Boolean)val;
                        }else if(val instanceof Integer){
                            Integer v = (Integer)val;
                        }else{
                            Double v = (Double)val;
                        }
                        break;
                    case "loc":
                        Integer loc = currentObject.getInt(k);
                        var.loc = loc;
                        break;
                    case "lines":
                        JSONArray lines = currentObject.getJSONArray(k);
                        var.lines = lines.toList().toString();
                        break;
                    default:
                        break;
                }
            }
            varList.add(var);
        }
        return FXCollections.observableArrayList(varList);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Integer getLoc() {
        return loc;
    }

    public void setLoc(Integer loc) {
        this.loc = loc;
    }

    public String getLines() {
        return lines;
    }

    public void setLines(String lines) {
        this.lines = lines;
    }
}
