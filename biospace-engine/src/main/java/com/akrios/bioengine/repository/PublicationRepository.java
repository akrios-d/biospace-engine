package com.akrios.bioengine.repository;


import com.akrios.bioengine.model.Publication;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PublicationRepository extends MongoRepository<Publication, String> {
    List<Publication> findByTitleContainingIgnoreCase(String keyword);
}