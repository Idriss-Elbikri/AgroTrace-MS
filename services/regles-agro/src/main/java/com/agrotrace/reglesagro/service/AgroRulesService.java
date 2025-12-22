package com.agrotrace.reglesagro.service;

import com.agrotrace.reglesagro.model.DonneesParcelle;
import com.agrotrace.reglesagro.model.Recommandation;
// Ajout des imports
import com.agrotrace.reglesagro.model.HistoriqueRecommandation;
import com.agrotrace.reglesagro.repository.HistoriqueRepository;

import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AgroRulesService {

    @Autowired
    private KieContainer kieContainer;

    // 1. On injecte le repository
    @Autowired
    private HistoriqueRepository historiqueRepository;

    public Recommandation analyserParcelle(DonneesParcelle donnees) {
        Recommandation recommandation = new Recommandation();
        recommandation.setAction("Aucune action requise");
        recommandation.setExplication("Conditions normales.");

        KieSession kieSession = kieContainer.newKieSession();
        kieSession.insert(donnees);
        kieSession.insert(recommandation);
        kieSession.fireAllRules();
        kieSession.dispose();

        // --- NOUVEAU : Sauvegarde en base de données ---
        HistoriqueRecommandation historique = new HistoriqueRecommandation(
                donnees.getHumiditeSol(),
                donnees.getTemperature(),
                donnees.getTypeCulture(),
                recommandation.getAction(),
                recommandation.getExplication()
        );

        historiqueRepository.save(historique);
        System.out.println(">>> Conseil sauvegardé en base de données !");
        // -----------------------------------------------

        return recommandation;
    }
}