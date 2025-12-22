package com.agrotrace.reglesagro.controller;

import com.agrotrace.reglesagro.model.DonneesParcelle;
import com.agrotrace.reglesagro.model.Recommandation;
import com.agrotrace.reglesagro.service.AgroRulesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/regles")
public class AgroRulesController {

    @Autowired
    private AgroRulesService agroRulesService;

    // POST : http://localhost:8080/api/regles/analyser
    @PostMapping("/analyser")
    public ResponseEntity<Recommandation> demanderRecommandation(@RequestBody DonneesParcelle donnees) {
        // On appelle le service (le cerveau)
        Recommandation resultat = agroRulesService.analyserParcelle(donnees);

        // On renvoie le résultat en JSON (Code 200 OK)
        return ResponseEntity.ok(resultat);
    }
}