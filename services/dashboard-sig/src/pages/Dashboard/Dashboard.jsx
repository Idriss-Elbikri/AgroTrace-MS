import { useState, useEffect, useCallback } from 'react';
import { MapView, Sidebar, Header, StatsBar } from '../../components';
import { parcellesService, previsionsService, visionService, irrigationService } from '../../services';
// SUPPRIMÉ : import { mockParcelles, mockPrevisions... } from '../../data/mockData';
import './Dashboard.css';

function Dashboard() {
  // États pour les données
  const [parcelles, setParcelles] = useState(null);
  const [selectedParcelle, setSelectedParcelle] = useState(null);
  const [previsions, setPrevisions] = useState(null);
  const [visionResults, setVisionResults] = useState(null);
  const [irrigationData, setIrrigationData] = useState(null);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [useMockData, setUseMockData] = useState(false); // Mode démo désactivé par défaut (car pas de mockData)

  // Statistiques
  const [stats, setStats] = useState({
    totalParcelles: 0,
    surfaceTotale: 0,
    parcellesCritiques: 0,
    irrigationUrgente: 0,
  });

  // Chargement des parcelles
  const loadParcelles = useCallback(async () => {
    try {
      setLoading(true);
      let data;

      if (useMockData) {
        // Utiliser les données de démo (VIDE POUR L'INSTANT)
        data = { type: "FeatureCollection", features: [] };
      } else {
        // Appel API réel
        // NOTE: Assure-toi que parcellesService gère les erreurs si l'API n'est pas encore prête
        data = await parcellesService.getGeoJSON().catch(e => {
          console.warn("API Parcelles non disponible, retour vide");
          return { type: "FeatureCollection", features: [] };
        });
      }

      setParcelles(data);

      // Calculer les statistiques
      if (data?.features) {
        const features = data.features;
        setStats({
          totalParcelles: features.length,
          surfaceTotale: features.reduce((acc, f) => acc + (f.properties?.surface || 0), 0),
          parcellesCritiques: features.filter(f => f.properties?.etat === 'critique').length,
          irrigationUrgente: features.filter(f => f.properties?.irrigationPrioritaire).length,
        });
      }
    } catch (err) {
      console.error('Erreur chargement parcelles:', err);
      setError('Impossible de charger les parcelles');
      setParcelles({ type: "FeatureCollection", features: [] });
    } finally {
      setLoading(false);
    }
  }, [useMockData]);

  // Chargement des détails quand une parcelle est sélectionnée
  const loadParcelleDetails = useCallback(async (parcelleId) => {
    try {
      if (useMockData) {
        // Données de démo (VIDES)
        setPrevisions([]);
        setVisionResults([]);
        setIrrigationData(null);
      } else {
        // Appels API parallèles
        const [previsionsData, visionData, irrigationDataRes] = await Promise.all([
          previsionsService.getByParcelle(parcelleId).catch(() => null),
          visionService.getByParcelle(parcelleId).catch(() => null),
          irrigationService.getByParcelle(parcelleId).catch(() => null),
        ]);

        setPrevisions(previsionsData);
        setVisionResults(visionData);
        setIrrigationData(irrigationDataRes);
      }
    } catch (err) {
      console.error('Erreur chargement détails parcelle:', err);
    }
  }, [useMockData]);

  // Chargement initial
  useEffect(() => {
    loadParcelles();
  }, [loadParcelles]);

  // Chargement des détails quand une parcelle est sélectionnée
  useEffect(() => {
    if (selectedParcelle?.id) {
      loadParcelleDetails(selectedParcelle.id);
    }
  }, [selectedParcelle, loadParcelleDetails]);

  // Gestion du clic sur une parcelle
  const handleParcelleClick = (properties) => {
    setSelectedParcelle(properties);
  };

  // Fermer le panneau latéral
  const handleCloseSidebar = () => {
    setSelectedParcelle(null);
    setPrevisions(null);
    setVisionResults(null);
    setIrrigationData(null);
  };

  // Gestion des filtres
  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  // Filtrer les parcelles
  const getFilteredParcelles = () => {
    if (!parcelles?.features || Object.keys(filters).every(k => !filters[k])) {
      return parcelles;
    }

    return {
      ...parcelles,
      features: parcelles.features.filter(feature => {
        const props = feature.properties;
        if (filters.culture && props.culture !== filters.culture) return false;
        if (filters.etat && props.etat !== filters.etat) return false;
        if (filters.irrigation && props.irrigationPriorite !== filters.irrigation) return false;
        return true;
      })
    };
  };

  return (
    <div className="dashboard">
      <Header
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      <StatsBar stats={stats} />

      <div className="dashboard-content">
        <div className="map-section">
          {loading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
              <p>Chargement des données...</p>
            </div>
          )}

          {error && !parcelles && (
            <div className="error-message">
              <p>⚠️ {error}</p>
              <button onClick={loadParcelles}>Réessayer</button>
            </div>
          )}

          <MapView
            parcelles={getFilteredParcelles()}
            onParcelleClick={handleParcelleClick}
            selectedParcelle={selectedParcelle}
          />
        </div>

        <Sidebar
          selectedParcelle={selectedParcelle}
          previsions={previsions}
          visionResults={visionResults}
          irrigationData={irrigationData}
          onClose={handleCloseSidebar}
        />
      </div>

      {/* Toggle mode démo (Désactivé pour l'instant car pas de mockData) */}
      {/* <div className="demo-toggle"> ... </div> */}
    </div>
  );
}

export default Dashboard;