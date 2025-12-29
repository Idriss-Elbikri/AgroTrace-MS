import { useState, useEffect, useCallback } from 'react';
import { MapView, Sidebar, Header, StatsBar } from '../../components';
import { parcellesService, previsionsService, visionService, irrigationService } from '../../services';
import './Dashboard.css';

function Dashboard() {
  const [parcelles, setParcelles] = useState(null);
  const [selectedParcelle, setSelectedParcelle] = useState(null);
  const [previsions, setPrevisions] = useState(null);
  const [visionResults, setVisionResults] = useState(null);
  const [irrigationData, setIrrigationData] = useState(null);
  const [filters, setFilters] = useState({ culture: '', etat: '', irrigation: '' });
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ totalParcelles: 0, surfaceTotale: 0, parcellesCritiques: 0, irrigationUrgente: 0 });

  // --- FONCTION : CHARGEMENT DES PARCELLES (POSTGIS) ---
  const loadParcelles = useCallback(async () => {
    try {
      setLoading(true);
      const data = await parcellesService.getGeoJSON();
      setParcelles(data);
      if (data?.features) {
        setStats({
          totalParcelles: data.features.length,
          surfaceTotale: data.features.reduce((acc, f) => acc + (f.properties?.surface || 0), 0),
          parcellesCritiques: 0,
          irrigationUrgente: 0
        });
      }
    } catch (e) {
      console.error("Erreur GeoJSON", e);
    } finally {
      setLoading(false);
    }
  }, []);

  // --- FONCTION : CHARGEMENT DÉTAILS (VISION & IRRIGATION) ---
  const loadParcelleDetails = useCallback(async (pid) => {
    const cleanId = String(pid).replace(/\D/g, '');
    console.log("🚀 Lancement du chargement pour l'ID nettoyé:", cleanId);

    try {
      const [vis, irrig] = await Promise.all([
        visionService.getByParcelle(cleanId).catch(() => null),
        irrigationService.getByParcelle(cleanId).catch(() => null),
      ]);

      console.log("✅ Données reçues du Backend:", { vis, irrig });

      setVisionResults(vis);
      setIrrigationData(irrig);

      if (irrig) {
        setPrevisions({
          temperature: irrig.temperature,
          humidite: irrig.humidite,
          vent: irrig.vent
        });
      }
    } catch (err) {
      console.error('❌ Erreur lors du chargement des détails:', err);
    }
  }, []);

  // --- LOGIQUE DES BOUTONS (HEADER) ---

  const handleRefresh = () => {
    console.log("🔄 Actualisation globale demandée...");
    setSelectedParcelle(null);
    loadParcelles();
  };

  // 2. Bouton Exporter (Génère un fichier CSV réel)
  const handleExport = () => {
    if (!selectedParcelle || !irrigationData) {
      alert("Veuillez sélectionner une parcelle avec des données pour exporter le rapport.");
      return;
    }

    // Préparation des données pour le CSV
    const rows = [
      ["Champ", "Valeur"],
      ["Nom de la parcelle", selectedParcelle.nom],
      ["Culture", selectedParcelle.culture],
      ["Surface (ha)", selectedParcelle.surface],
      ["Temperature (°C)", irrigationData.temperature],
      ["Humidite (%)", irrigationData.humidite],
      ["Etat du sol", irrigationData.etat],
      ["Indice NDVI", visionResults?.ndvi || "N/A"],
      ["Sante Vegetale (%)", visionResults?.santeVegetale || "N/A"],
      ["Conseil Irrigation", irrigationData.recommandation],
      ["Date Export", new Date().toLocaleString()]
    ];

    // Création du contenu CSV
    const csvContent = "data:text/csv;charset=utf-8,"
      + rows.map(e => e.join(",")).join("\n");

    // Création d'un lien de téléchargement invisible
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `Rapport_AgroTrace_Parcelle_${selectedParcelle.id}.csv`);
    document.body.appendChild(link);

    // Déclenchement du téléchargement
    link.click();
    document.body.removeChild(link);

    console.log("✅ Fichier CSV généré et téléchargé.");
  };

  // --- LOGIQUE DE FILTRAGE DYNAMIQUE ---
  // On filtre les features GeoJSON avant de les envoyer à la MapView
  const filteredParcelles = parcelles && parcelles.features ? {
    ...parcelles,
    features: parcelles.features.filter(f => {
      // Filtre par Culture (Blé, Maïs, etc.)
      const cultureMatch = !filters.culture || f.properties.culture === filters.culture;

      // Filtre par État (Excellent, Bon, etc. - basé sur les properties PostGIS)
      const etatMatch = !filters.etat || f.properties.etat === filters.etat;

      return cultureMatch && etatMatch;
    })
  } : parcelles;

  // --- EFFETS ---
  useEffect(() => {
    loadParcelles();
  }, [loadParcelles]);

  useEffect(() => {
    const pid = selectedParcelle?.id || selectedParcelle?.sensor_id;
    if (pid) {
      loadParcelleDetails(pid);
    }
  }, [selectedParcelle?.id, selectedParcelle?.sensor_id, loadParcelleDetails]);

  // --- HANDLERS ---
  const handleParcelleClick = (props) => {
    console.log("🖱️ Clic détecté sur:", props);
    const rawId = props.id || props.sensor_id;
    const cleanId = String(rawId).replace(/\D/g, '');
    setSelectedParcelle({ ...props, id: cleanId });
  };

  return (
    <div className="dashboard">
      <Header
        filters={filters}
        onFilterChange={(n, v) => setFilters(p => ({ ...p, [n]: v }))}
        onRefresh={handleRefresh}
        onExport={handleExport}
      />

      <StatsBar stats={stats} />

      <div className="dashboard-content">
        <div className="map-section">
          {loading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
            </div>
          )}
          <MapView
            parcelles={filteredParcelles} // On passe les données filtrées
            onParcelleClick={handleParcelleClick}
            selectedParcelle={selectedParcelle}
          />
        </div>

        <Sidebar
          selectedParcelle={selectedParcelle}
          previsions={previsions}
          visionResults={visionResults}
          irrigationData={irrigationData}
          onClose={() => setSelectedParcelle(null)}
        />
      </div>
    </div>
  );
}

export default Dashboard;