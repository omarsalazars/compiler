package sample;

import javafx.application.Platform;
import org.fxmisc.richtext.CodeArea;
import org.fxmisc.richtext.GenericStyledArea;
import org.fxmisc.richtext.model.Paragraph;
import org.fxmisc.richtext.model.StyleSpans;
import org.fxmisc.richtext.model.StyleSpansBuilder;
import org.reactfx.collection.ListModification;

import java.util.Collection;
import java.util.Collections;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SyntaxHighlighter {

    private VisibleParagraphStyler styler;
    private CodeArea editor;

    private static final String[] KEYWORDS = new String[] {
            "if", "else", "do", "while", "repeat", "until"
    };

    private static final String[] LITERAL = new String[]{
            "true", "false"
    };

    private static final String[] TYPE = new String[]{
            "int", "bool", "float"
    };

    private static final String KEYWORD_PATTERN = "\\b(" + String.join("|", KEYWORDS) + ")\\b";
    private static final String PAREN_PATTERN = "\\(|\\)";
    private static final String BRACE_PATTERN = "\\{|\\}";
    private static final String SEMICOLON_PATTERN = "\\;";
    private static final String FLOAT_PATTERN = "\\d+.\\d+";
    private static final String NUMBER_PATTERN = "\\d+";
    private static final String LITERAL_PATTERN = "\\b(" + String.join("|", LITERAL) + ")\\b";
    private static final String TYPE_PATTERN = "\\b(" + String.join("|", TYPE) + ")\\b";

    private static final Pattern PATTERN = Pattern.compile(
            "(?<KEYWORD>" + KEYWORD_PATTERN +")"
                    + "|(?<PAREN>" + PAREN_PATTERN + ")"
                    + "|(?<BRACE>" + BRACE_PATTERN + ")"
                    + "|(?<SEMICOLON>" + SEMICOLON_PATTERN + ")"
                    + "|(?<FLOAT>" + FLOAT_PATTERN + ")"
                    + "|(?<NUMBER>" + NUMBER_PATTERN + ")"
                    + "|(?<LITERAL>" + LITERAL_PATTERN + ")"
                    + "|(?<TYPE>" + TYPE_PATTERN + ")"
    );

    public SyntaxHighlighter(CodeArea editor){
        this.editor = editor;
    }

    private StyleSpans<Collection<String>> computeHighlighting(String text){
        Matcher matcher = PATTERN.matcher(text);
        int lastKwEnd = 0;
        StyleSpansBuilder<Collection<String>> spansBuilder = new StyleSpansBuilder<>();
        while(matcher.find()){
            String styleClass =
                    matcher.group("KEYWORD") != null ? "keyword":
                            matcher.group("PAREN") != null ? "paren":
                                    matcher.group("BRACE") != null ? "brace":
                                            matcher.group("SEMICOLON") != null ? "semi":
                                                    matcher.group("FLOAT") != null ? "float":
                                                            matcher.group("NUMBER") != null ? "number":
                                                                    matcher.group("LITERAL") != null ? "literal" :
                                                                            matcher.group("TYPE") != null ? "type" : null;
            assert styleClass != null;
            spansBuilder.add(Collections.emptyList(), matcher.start() - lastKwEnd);
            spansBuilder.add(Collections.singleton(styleClass), matcher.end() - matcher.start());
            lastKwEnd = matcher.end();
        }
        spansBuilder.add(Collections.emptyList(), text.length() - lastKwEnd);
        return spansBuilder.create();
    }

    public VisibleParagraphStyler getSyntaxStyler(){
        if( styler == null ){
            styler = new VisibleParagraphStyler<>(editor, this::computeHighlighting);
        }
        return styler;
    }

    private class VisibleParagraphStyler<PS, SEG, S> implements Consumer<ListModification<? extends Paragraph<PS, SEG, S>>>
    {

        private final GenericStyledArea<PS, SEG, S> area;
        private final Function<String, StyleSpans<S>> computeStyles;
        private int prevParagraph, prevTextLength;

        public VisibleParagraphStyler(GenericStyledArea<PS, SEG, S> area, Function<String, StyleSpans<S>> computeStyles){
            this.computeStyles = computeStyles;
            this.area = area;
        }

        @Override
        public void accept(ListModification<? extends Paragraph<PS, SEG, S>> lm) {
            if(lm.getAddedSize() > 0){
                int paragraph = Math.min( area.firstVisibleParToAllParIndex()+lm.getFrom(), area.getParagraphs().size()-1 );
                String text = area.getText(paragraph, 0, paragraph, area.getParagraphLength(paragraph));

                if( paragraph != prevParagraph || text.length() != prevTextLength){
                    int startPos = area.getAbsolutePosition(paragraph, 0);
                    Platform.runLater( () -> area.setStyleSpans(startPos, computeStyles.apply(text)) );
                    prevTextLength = text.length();
                    prevParagraph = paragraph;
                }
            }
        }
    }
}
