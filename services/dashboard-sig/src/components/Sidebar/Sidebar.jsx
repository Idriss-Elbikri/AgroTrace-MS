import './Sidebar.css';

function Sidebar({ 
  selectedParcelle, 
  previsions, 
  visionResults, 
  irrigationData,
  onClose 
}) {
  if (!selectedParcelle) {
    return (
      <div className="sidebar">
        <div className="sidebar-empty">
          <div className="empty-icon">🗺️</div>
          <h3>Sélectionnez une parcelle</h3>
          <p>Cliquez sur une parcelle sur la carte pour voir ses détails</p>
        </div>
      </div>
    );
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>{selectedParcelle.nom || 'Parcelle'}</h2>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      
      {/* Informations générales */}
      <section className="sidebar-section">
        <h3>📍 Informations générales</h3>
        <div className="info-grid">
          <div className="info-item">
            <span className="info-label">Surface</span>
            <span className="info-value">{selectedParcelle.surface || 'N/A'} ha</span>
          </div>
          <div className="info-item">
            <span className="info-label">Culture</span>
            <span className="info-value">{selectedParcelle.culture || 'N/A'}</span>
          </div>
          <div className="info-item">
            <span className="info-label">État</span>
            <span className={`info-value etat-${selectedParcelle.etat}`}>
              {selectedParcelle.etat || 'N/A'}
            </span>
          </div>
          <div className="info-item">
            <span className="info-label">Propriétaire</span>
            <span className="info-value">{selectedParcelle.proprietaire || 'N/A'}</span>
          </div>
        </div>
      </section>
      
      {/* Prévisions météo */}
      <section className="sidebar-section">
        <h3>🌤️ Prévisions météo</h3>
        {previsions ? (
          <div className="weather-info">
            <div className="weather-current">
              <span className="weather-temp">{previsions.temperature || '--'}°C</span>
              <span className="weather-desc">{previsions.description || 'N/A'}</span>
            </div>
            <div className="weather-details">
              <div className="weather-item">
                <span>💧 Humidité</span>
                <span>{previsions.humidite || '--'}%</span>
              </div>
              <div className="weather-item">
                <span>💨 Vent</span>
                <span>{previsions.vent || '--'} km/h</span>
              </div>
              <div className="weather-item">
                <span>🌧️ Précipitations</span>
                <span>{previsions.precipitations || '--'} mm</span>
              </div>
            </div>
          </div>
        ) : (
          <p className="no-data">Aucune prévision disponible</p>
        )}
      </section>
      
      {/* Résultats de vision */}
      <section className="sidebar-section">
        <h3>📸 Analyse vision</h3>
        {visionResults ? (
          <div className="vision-info">
            <div className="vision-status">
              <span className={`status-badge status-${visionResults.statut}`}>
                {visionResults.statut || 'N/A'}
              </span>
            </div>
            <div className="vision-details">
              <p><strong>Dernière analyse:</strong> {visionResults.date || 'N/A'}</p>
              <p><strong>Santé végétale:</strong> {visionResults.santeVegetale || 'N/A'}%</p>
              <p><strong>NDVI moyen:</strong> {visionResults.ndvi || 'N/A'}</p>
              {visionResults.alertes && visionResults.alertes.length > 0 && (
                <div className="vision-alerts">
                  <strong>Alertes:</strong>
                  <ul>
                    {visionResults.alertes.map((alerte, index) => (
                      <li key={index} className="alert-item">{alerte}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ) : (
          <p className="no-data">Aucune analyse disponible</p>
        )}
      </section>
      
      {/* Recommandations d'irrigation */}
      <section className="sidebar-section">
        <h3>💧 Irrigation</h3>
        {irrigationData ? (
          <div className="irrigation-info">
            <div className={`irrigation-status status-${irrigationData.priorite}`}>
              <span className="irrigation-icon">
                {irrigationData.priorite === 'haute' ? '🔴' : 
                 irrigationData.priorite === 'moyenne' ? '🟡' : '🟢'}
              </span>
              <span>Priorité: {irrigationData.priorite || 'N/A'}</span>
            </div>
            <div className="irrigation-details">
              <p><strong>Recommandation:</strong></p>
              <p className="recommendation-text">{irrigationData.recommandation || 'Aucune recommandation'}</p>
              <div className="irrigation-metrics">
                <div className="metric">
                  <span className="metric-label">Eau nécessaire</span>
                  <span className="metric-value">{irrigationData.quantite || '--'} L/m²</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Prochaine irrigation</span>
                  <span className="metric-value">{irrigationData.prochaineDate || 'N/A'}</span>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <p className="no-data">Aucune donnée d'irrigation disponible</p>
        )}
      </section>
    </div>
  );
}

export default Sidebar;
