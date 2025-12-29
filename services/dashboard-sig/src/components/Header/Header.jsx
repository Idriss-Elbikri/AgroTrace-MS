import './Header.css';

// AJOUT : onRefresh et onExport dans les arguments de la fonction
function Header({ onFilterChange, filters, onRefresh, onExport }) {
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
            <option value="Blé">Blé</option>
            <option value="Maïs">Maïs</option>
            <option value="Olivier">Olivier</option>
            <option value="Agrumes">Agrumes</option>
            <option value="Tomate">Tomate</option>
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
            <option value="Excellent">Excellent</option>
            <option value="Bon">Bon</option>
            <option value="Moyen">Moyen</option>
            <option value="Attention">Attention</option>
            <option value="Critique">Critique</option>
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
        {/* MODIFICATION : Ajout du onClick={onRefresh} */}
        <button className="btn-refresh" onClick={onRefresh} title="Actualiser les données">
          🔄 Actualiser
        </button>
        {/* MODIFICATION : Ajout du onClick={onExport} */}
        <button className="btn-export" onClick={onExport} title="Exporter les données">
          📥 Exporter
        </button>
      </div>
    </header>
  );
}

export default Header;