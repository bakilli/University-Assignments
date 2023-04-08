package com.yazlab.stringconcat;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Document(collection = "strings")
public class Strings {
    @Id
    public String id;
    public List<String> strings;
    public String result;

    public double duration;

    public Strings() {}
    public Strings(List<String> strings, String result, double duration) {
        this.strings = strings;
        this.result = result;
        this.duration = duration;
    }

}
