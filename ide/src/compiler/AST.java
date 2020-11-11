package compiler;

import javafx.scene.control.TreeItem;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

public class AST {
    private JSONObject json;

    public AST(String json){
        this.json = new JSONObject(json);
    }

    public TreeItem<String> toTreeNode(){
        TreeItem<String> root = new TreeItem<>("main");
        root.getChildren().addAll(visitNode(root, json));
        return root;
    }

    private Collection<? extends TreeItem<String>> visitNode(TreeItem<String> parent, Object node){
        ArrayList<TreeItem<String>> list = new ArrayList<>();
        if(node instanceof JSONObject){
            JSONObject obj = (JSONObject)node;
            Iterator<String> it = obj.keys();
            while (it.hasNext()){
                String nextString = it.next();
                System.out.println(nextString);
                if(nextString.equals("prod")) continue;
                Object next = obj.get(nextString);
                String nextNodeName = nextString;
                if(next instanceof JSONObject){
                    JSONObject aux = (JSONObject) next;
                    if(aux.has("val")) {
                        Object o = aux.get("val");
                        nextNodeName += " val: " + o.toString();
                    }
                }
                else if(nextString.equals("token")){ //Check if nextNode is token
                    JSONObject token = obj.optJSONObject("token");
                    if(token!=null){
                        String type = token.getString("type");
                        String val = "";
                        if(type.equals("number") || type.equals("float")){
                            val = token.getString("val");
                            nextNodeName += " val: "+val;
                        }
                    }
                }
                else if(nextString.equals("op")){ //Operator node
                    JSONObject operator = obj.getJSONObject("op");
                    String val = operator.getString("val");
                    nextNodeName += " val: "+val;
                }
                TreeItem<String> nextNode = new TreeItem<>(nextNodeName);
                nextNode.getChildren().addAll(visitNode(new TreeItem<>(nextString), next));
                list.add(nextNode);
            }
        }else if(node instanceof JSONArray){
            JSONArray array = (JSONArray)node;
            Iterator<Object> it = array.iterator();
            while(it.hasNext()){
                Object next = it.next();
                TreeItem<String> nextNode = new TreeItem<>(parent.getValue().substring(0, parent.getValue().length()-1));
                if(next instanceof JSONObject){
                    JSONObject obj = (JSONObject)next;
                    if(obj.has("prod")){
                        nextNode.setValue(obj.optString("prod"));
                    }
                }
                nextNode.getChildren().addAll(visitNode(new TreeItem<>(parent.getValue()), next));
                list.add(nextNode);
            }
        }else{
            list.add(new TreeItem<>(node.toString()));
        }
        return list;
    }
}
