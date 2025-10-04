package com.akrios.bioengine.repository;


import com.akrios.bioengine.model.Publication;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PublicationRepository extends MongoRepository<Publication, String> {
    List<Publication> findByTitleContainingIgnoreCase(String keyword);

    @Query("""
    {
      title: { $exists: true, $ne: "" },
      abstractText: { $exists: true, $ne: "" },
      tags: { $ne: "correction" }
    }
    """)
    List<Publication> findValidPublications();
}