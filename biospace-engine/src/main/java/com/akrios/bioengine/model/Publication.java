package com.akrios.bioengine.model;


import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Document(collection = "publications")
@Getter
@Setter
public class Publication {

    @Id
    private String id;
    private String title;
    private String link;
    private String abstractText;
    private List<String> tags;
    private double score;
    private String resultsSection;
    private String conclusionsSection;
}
