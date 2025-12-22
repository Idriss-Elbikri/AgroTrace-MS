package com.agrotrace.reglesagro.model;

public class Recommandation {

    private String action;        // ex: "Irrigation Urgente"
    private String explication;   // ex: "Car il fait trop chaud"

    public Recommandation() {}

    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }

    public String getExplication() { return explication; }
    public void setExplication(String explication) { this.explication = explication; }
}