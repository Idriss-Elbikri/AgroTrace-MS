package com.agrotrace.reglesagro.model;

public class DonneesParcelle {

    private Double humiditeSol;
    private Double temperature;
    private String typeCulture;   // ex: "Blé"
    private String stadeCroissance; // ex: "Floraison"
    private String typeSol; // ex: "Argileux", "Sableux"

    // Constructeur vide (obligatoire pour Spring)
    public DonneesParcelle() {}

    // Constructeur complet
    public DonneesParcelle(Double humiditeSol, Double temperature, String typeCulture, String stadeCroissance, String typeSol) {
        this.humiditeSol = humiditeSol;
        this.temperature = temperature;
        this.typeCulture = typeCulture;
        this.stadeCroissance = stadeCroissance;
        this.typeSol = typeSol;
    }

    // Getters et Setters
    public Double getHumiditeSol() { return humiditeSol; }
    public void setHumiditeSol(Double humiditeSol) { this.humiditeSol = humiditeSol; }

    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }

    public String getTypeCulture() { return typeCulture; }
    public void setTypeCulture(String typeCulture) { this.typeCulture = typeCulture; }

    public String getStadeCroissance() { return stadeCroissance; }
    public void setStadeCroissance(String stadeCroissance) { this.stadeCroissance = stadeCroissance; }

    public String getTypeSol() { return typeSol; }
    public void setTypeSol(String typeSol) { this.typeSol = typeSol; }
}