package com.agrotrace.reglesagro.repository;

import com.agrotrace.reglesagro.model.HistoriqueRecommandation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface HistoriqueRepository extends JpaRepository<HistoriqueRecommandation, Long> {
    // C'est tout ! Spring fournit automatiquement la méthode .save()
}