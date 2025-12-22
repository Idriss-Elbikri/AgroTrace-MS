package com.agrotrace.reglesagro.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "historique_conseils")
public class HistoriqueRecommandation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDateTime dateConseil;

    // On garde une trace de ce qui a provoqué le conseil
    private Double humiditeEnregistree;
    private Double temperatureEnregistree;
    private String culture;

    // Le conseil donné
    private String actionRecommandee;
    @Column(length = 1000) // Pour permettre un texte long
    private String explication;

    public HistoriqueRecommandation() {}

    // Constructeur pratique
    public HistoriqueRecommandation(Double hum, Double temp, String cult, String action, String expl) {
        this.dateConseil = LocalDateTime.now(); // Date automatique
        this.humiditeEnregistree = hum;
        this.temperatureEnregistree = temp;
        this.culture = cult;
        this.actionRecommandee = action;
        this.explication = expl;
    }

    // Getters et Setters (Générés par IDE ou copiés ici)
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    // ... Tu peux générer les autres getters/setters si besoin, mais le constructeur suffit pour sauvegarder.
}