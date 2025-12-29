import React from 'react';
import './Sidebar.css';

/**
 * Composant Sidebar : Affiche les données IoT, Vision et Irrigation 
 * synchronisées via la Gateway Nginx.
 */
function Sidebar({ selectedParcelle, irrigationData, previsions, visionResults, onClose }) {
  // État initial : Aucune parcelle sélectionnée
  if (!selectedParcelle) {
    return (
      <div className="sidebar">
        <div className="sidebar-empty">
          <div className="empty-icon">🗺️</div>
          <h3>Sélectionnez une parcelle</h3>
          <p>Cliquez sur une zone de la carte pour charger les données capteurs.</p>
        </div>
      </div>
    );
  }

  // --- LOGIQUE DE SÉCURITÉ ---
  const isDataValid = irrigationData && typeof irrigationData === 'object' && irrigationData.temperature;

  // Préparation des données (Fusion des données API et des fallbacks)
  const display = {
    temperature: isDataValid ? irrigationData.temperature : (previsions?.temperature || '--'),
    humidite: isDataValid ? irrigationData.humidite : (previsions?.humidite || '--'),
    vent: irrigationData?.vent || '12.4',
    etat: isDataValid ? irrigationData.etat : 'Analyse...', // "Sec", "Optimal" ou "Saturé"
    recommandation: isDataValid ? irrigationData.recommandation : 'Moteur Drools : Calcul en cours...',
    volume: isDataValid ? (irrigationData.quantite || '0') : '0',
    sante: visionResults?.santeVegetale || '85',
    ndvi: visionResults?.ndvi || '0.72',
    alertes: visionResults?.alertes || [] // Récupération de la liste des alertes réelles
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="header-title">
          <h2>{selectedParcelle.nom || 'Détails Parcelle'}</h2>
          <span className="id-badge">ID: {selectedParcelle.id}</span>
        </div>
        <button className="close-btn" onClick={onClose} title="Fermer">×</button>
      </div>

      <div className="sidebar-scroll-content">

        {/* Section 1 : Informations Générales (PostGIS) */}
        <section className="sidebar-section">
          <h3>📍 Informations Générales</h3>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Surface:</span>
              <span className="value">{selectedParcelle.surface || selectedParcelle.surface_ha || '0'} ha</span>
            </div>
            <div className="info-item">
              <span className="label">Culture:</span>
              <span className="value">{selectedParcelle.culture || 'Blé'}</span>
            </div>
            <div className="info-item">
              <span className="label">État Sol:</span>
              {/* Le style CSS change selon la valeur : sec, optimal, saturé */}
              <span className={`value status-${display.etat.split(' ')[0].toLowerCase()}`}>
                {display.etat}
              </span>
            </div>
          </div>
        </section>

        {/* Section 2 : Météo Temps Réel (IoT Kafka/Timescale) */}
        <section className="sidebar-section">
          <h3>🌤️ Météo Temps Réel</h3>
          <div className="weather-card">
            <div className="weather-main">
              <span className="temp-value">{display.temperature}°C</span>
              <span className="weather-desc">Capteurs Actifs</span>
            </div>
            <div className="weather-stats">
              <div className="stat">
                <span className="stat-icon">💧</span>
                <span className="stat-label">Humidité: {display.humidite}%</span>
              </div>
              <div className="stat">
                <span className="stat-icon">💨</span>
                <span className="stat-label">Vent: {display.vent} km/h</span>
              </div>
            </div>
          </div>
        </section>

        {/* Section 3 : Analyse Vision (CNN UAV) */}
        <section className="sidebar-section">
          <h3>📸 Vision UAV & Santé</h3>
          <div className="vision-box">
            <div className="vision-stat">
              <span className="label">Santé Végétale</span>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${display.sante}%` }}></div>
              </div>
              <span className="percent">{display.sante}%</span>
            </div>
            <div className="vision-stat">
              <span className="label">Indice NDVI</span>
              <span className="value">{display.ndvi}</span>
            </div>

            {/* AJOUT : Liste des alertes UAV dynamiques */}
            {display.alertes.length > 0 && (
              <div className="uav-alerts">
                <span className="label">Alertes UAV :</span>
                <ul>
                  {display.alertes.map((alerte, index) => (
                    <li key={index} className="alert-item">⚠️ {alerte}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </section>

        {/* Section 4 : Recommandations (Drools Java) */}
        <section className="sidebar-section recommendation-section">
          <h3>💧 Conseil d'Irrigation</h3>
          <div className="reco-card">
            <p className="reco-text">"{display.recommandation}"</p>
            <div className="reco-metrics">
              <div className="metric">
                <span className="label">Volume</span>
                <span className="value">{display.volume} L/m²</span>
              </div>
              <div className="metric">
                <span className="label">Priorité</span>
                <span className="value priority-badge">
                  {display.volume > 0 ? 'Haute' : 'Basse'}
                </span>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}

export default Sidebar;