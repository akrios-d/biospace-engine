package com.akrios.bioengine.service;

import com.akrios.bioengine.model.Publication;
import com.akrios.bioengine.model.QueryRequest;
import com.akrios.bioengine.repository.PublicationRepository;
import org.apache.commons.text.similarity.LevenshteinDistance;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class OptimizationService {

    private final PublicationRepository repo;

    public OptimizationService(PublicationRepository repo) {
        this.repo = repo;
    }

    /**
     * Score simples: combina correspondências de termos (title+abstract),
     * peso por perfil e um pequeno bónus para títulos curtos (mais diretos).
     *
     * Extende-se facilmente para TF-IDF, NLP, OR-Tools ou OptaPlanner.
     */
    public List<Publication> query(QueryRequest req) {
        String query = Optional.ofNullable(req.getQuery()).orElse("").toLowerCase();
        String[] terms = query.isBlank() ? new String[0] : query.split("\\s+");

        List<Publication> pubs = new ArrayList<>(repo.findAll());

        for (Publication p : pubs) {
            double matchScore = computeMatchScore(p, terms);
            double profileBonus = profileBonus(req.getProfile(), p);
            double lenBonus = titleLengthBonus(p);
            double total = 0.75 * matchScore + 0.15 * profileBonus + 0.10 * lenBonus;
            p.setScore(total);
        }

        // sort desc by score

        return pubs.stream()
                .sorted(Comparator.comparingDouble(Publication::getScore).reversed())
                .limit(req.getK() <= 0 ? 20 : req.getK())
                .collect(Collectors.toList());
    }

    private double computeMatchScore(Publication p, String[] terms) {
        if (terms.length == 0) return 0.0;
        String hay = (p.getTitle() + " " + p.getAbstractText()).toLowerCase();
        int matches = 0;
        for (String t : terms) {
            if (t.isBlank()) continue;
            if (hay.contains(t)) matches++;
            else {
                // fuzzy attempt: small edit distance on words
                String[] words = hay.split("\\W+");
                for (String w : words) {
                    if (w.length() > 3) {
                        int dist = LevenshteinDistance.getDefaultInstance().apply(t, w);
                        if (dist <= 1) { matches++; break; }
                    }
                }
            }
        }
        return (double) matches / (double) terms.length; // 0..1
    }

    private double profileBonus(String profile, Publication p) {
        if (profile == null) profile = "scientist";
        profile = profile.toLowerCase();
        switch (profile) {
            case "scientist": return 0.1;
            case "manager": return 0.06;
            case "architect": return 0.08;
            default: return 0.05;
        }
    }

    private double titleLengthBonus(Publication p) {
        int len = Optional.ofNullable(p.getTitle()).orElse("").length();
        if (len < 50) return 0.06;
        if (len < 120) return 0.03;
        return 0.0;
    }
}