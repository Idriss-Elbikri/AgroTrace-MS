import './Header.css';

function Header({ onFilterChange, filters }) {
  return (
    <header className="dashboard-header">
      <div className="header-brand">
        <span className="brand-icon">🌱</span>
        <h1>AgroTrace SIG</h1>
        <span className="brand-subtitle">Dashboard Cartographique</span>
      </div>
      
      <div className="header-filters">
        <div className="filter-group">
          <label htmlFor="filter-culture">Culture</label>
          <select 
            id="filter-culture"
            value={filters?.culture || ''} 
            onChange={(e) => onFilterChange?.('culture', e.target.value)}
          >
            <option value="">Toutes</option>
            <option value="ble">Blé</option>
            <option value="mais">Maïs</option>
            <option value="olivier">Olivier</option>
            <option value="agrumes">Agrumes</option>
            <option value="tomate">Tomate</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="filter-etat">État</label>
          <select 
            id="filter-etat"
            value={filters?.etat || ''} 
            onChange={(e) => onFilterChange?.('etat', e.target.value)}
          >
            <option value="">Tous</option>
            <option value="excellent">Excellent</option>
            <option value="bon">Bon</option>
            <option value="moyen">Moyen</option>
            <option value="attention">Attention</option>
            <option value="critique">Critique</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="filter-irrigation">Irrigation</label>
          <select 
            id="filter-irrigation"
            value={filters?.irrigation || ''} 
            onChange={(e) => onFilterChange?.('irrigation', e.target.value)}
          >
            <option value="">Toutes</option>
            <option value="haute">Priorité haute</option>
            <option value="moyenne">Priorité moyenne</option>
            <option value="basse">Priorité basse</option>
          </select>
        </div>
      </div>
      
      <div className="header-actions">
        <button className="btn-refresh" title="Actualiser les données">
          🔄 Actualiser
        </button>
        <button className="btn-export" title="Exporter les données">
          📥 Exporter
        </button>
      </div>
    </header>
  );
}

export default Header;
