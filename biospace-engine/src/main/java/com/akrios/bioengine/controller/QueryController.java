package com.akrios.bioengine.controller;

import com.akrios.bioengine.model.Publication;
import com.akrios.bioengine.model.QueryRequest;
import com.akrios.bioengine.service.OptimizationService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
public class QueryController {

    private final OptimizationService service;

    public QueryController(OptimizationService service) {
        this.service = service;
    }

    @PostMapping("/query")
    public List<Publication> query(@RequestBody QueryRequest req) {
        return service.query(req);
    }
}
