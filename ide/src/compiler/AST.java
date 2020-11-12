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
        TreeItem<String> statements = root.getChildren().get(0);
        TreeItem<String> decl = root.getChildren().get(1);
        root.getChildren().clear();
        root.getChildren().add(decl);
        root.getChildren().add(statements);
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
                TreeItem<String> nextNode = new TreeItem<>(nextNodeName);
                nextNode.getChildren().addAll(visitNode(new TreeItem<>(nextString), next));
                list.add(nextNode);
            }
        }else if(node instanceof JSONArray){
           /* JSONArray array = (JSONArray)node;
            Iterator<Object> it = array.iterator();
            while(it.hasNext()){
                Object next = it.next();
                TreeItem<String> nextNode = new TreeItem<>(parent.getValue().substring(0, parent.getValue().length()-1));
                if(next instanceof JSONObject){
                    JSONObject obj = (JSONObject)next;
                    if(obj.has("prod")){
                        nextNode.setValue(obj.optString("prod"));
                    }else if(obj.length()==1){
                        Iterator<String> it2 = obj.keys();
                        String x = it2.next();
                        nextNode.setValue(x);
                        nextNode.getChildren().addAll(visitNode(nextNode, obj.get(x)));
                    }
                }else {
                    nextNode.getChildren().addAll(visitNode(new TreeItem<>(parent.getValue()), next));
                    list.add(nextNode);
                }
            }*/
            JSONArray array = (JSONArray)node;
            Iterator<Object> it = array.iterator();
            while(it.hasNext()){
                Object next = it.next();
                TreeItem<String> treeItem = new TreeItem<>();
                if(next instanceof JSONObject){
                    JSONObject obj = (JSONObject) next;
                    if(obj.has("prod")){
                        treeItem.setValue(obj.getString("prod"));
                        Iterator<String> it2 = obj.keys();
                        while(it2.hasNext()){
                            String aux = it2.next();
                            if(aux.equals("prod")) continue;
                            treeItem.getChildren().addAll(visitNode(treeItem, obj.get(aux)));
                        }
                        list.add(treeItem);
                    }else if(obj.length()==1){
                        Iterator<String> it2 = obj.keys();
                        String name = it2.next();
                        treeItem.setValue(name);
                        treeItem.getChildren().addAll(visitNode(treeItem, obj.get(name)));
                        list.add(treeItem);
                    }else{
                        Iterator<String> it2 = obj.keys();
                        while(it2.hasNext()){
                            treeItem.getChildren().addAll(visitNode(treeItem, obj.get(it2.next())));
                        }
                        list.add(treeItem);
                    }
                }else{
                    treeItem.setValue(next.toString());
                    treeItem.getChildren().addAll(visitNode(treeItem, next));
                    list.add(treeItem);
                }
            }
        }else{
            list.add(new TreeItem<>(node.toString()));
        }
        return list;
    }
}
