import './StatsBar.css';

function StatsBar({ stats }) {
  const defaultStats = {
    totalParcelles: 0,
    surfaceTotale: 0,
    parcellesCritiques: 0,
    irrigationUrgente: 0,
    ...stats
  };

  return (
    <div className="stats-bar">
      <div className="stat-item">
        <span className="stat-icon">🗺️</span>
        <div className="stat-content">
          <span className="stat-value">{defaultStats.totalParcelles}</span>
          <span className="stat-label">Parcelles</span>
        </div>
      </div>
      
      <div className="stat-item">
        <span className="stat-icon">📐</span>
        <div className="stat-content">
          <span className="stat-value">{defaultStats.surfaceTotale}</span>
          <span className="stat-label">Hectares</span>
        </div>
      </div>
      
      <div className="stat-item stat-warning">
        <span className="stat-icon">⚠️</span>
        <div className="stat-content">
          <span className="stat-value">{defaultStats.parcellesCritiques}</span>
          <span className="stat-label">État critique</span>
        </div>
      </div>
      
      <div className="stat-item stat-danger">
        <span className="stat-icon">💧</span>
        <div className="stat-content">
          <span className="stat-value">{defaultStats.irrigationUrgente}</span>
          <span className="stat-label">Irrigation urgente</span>
        </div>
      </div>
    </div>
  );
}

export default StatsBar;
