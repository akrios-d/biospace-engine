package com.akrios.bioengine.controller;

import com.akrios.bioengine.model.Publication;
import com.akrios.bioengine.repository.PublicationRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/publications")
public class PublicationController {

    private final PublicationRepository repo;

    public PublicationController(PublicationRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public List<Publication> all() {
        return repo.findValidPublications();
    }

    @GetMapping("/{id}")
    public Publication getById(@PathVariable String id) {
        return repo.findById(id).orElseThrow(() -> new ResourceNotFoundException("Not found"));
    }

    @ResponseStatus(code = org.springframework.http.HttpStatus.NOT_FOUND)
    static class ResourceNotFoundException extends RuntimeException {
        public ResourceNotFoundException(String msg) { super(msg); }
    }
}
