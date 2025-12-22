import { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './MapView.css';

// Fix pour les icônes Leaflet avec Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Composant pour recentrer la carte sur les données
function FitBounds({ geoJsonData }) {
  const map = useMap();
  
  useEffect(() => {
    if (geoJsonData && geoJsonData.features?.length > 0) {
      const geoJsonLayer = L.geoJSON(geoJsonData);
      map.fitBounds(geoJsonLayer.getBounds(), { padding: [20, 20] });
    }
  }, [geoJsonData, map]);
  
  return null;
}

// Fonction pour déterminer la couleur selon l'état de la parcelle
const getParcelleColor = (etat) => {
  switch (etat) {
    case 'excellent':
      return '#22c55e'; // Vert
    case 'bon':
      return '#84cc16'; // Vert clair
    case 'moyen':
      return '#eab308'; // Jaune
    case 'attention':
      return '#f97316'; // Orange
    case 'critique':
      return '#ef4444'; // Rouge
    default:
      return '#6b7280'; // Gris
  }
};

// Style pour les parcelles GeoJSON
const parcelleStyle = (feature) => ({
  fillColor: getParcelleColor(feature.properties?.etat),
  weight: 2,
  opacity: 1,
  color: '#ffffff',
  dashArray: '',
  fillOpacity: 0.7,
});

// Style au survol
const highlightStyle = {
  weight: 3,
  color: '#2563eb',
  dashArray: '',
  fillOpacity: 0.9,
};

function MapView({ 
  parcelles, 
  onParcelleClick, 
  selectedParcelle,
  overlayData,
  showVision,
  showIrrigation,
  showPrevisions 
}) {
  const geoJsonRef = useRef();
  const [map, setMap] = useState(null);
  
  // Centre par défaut (Maroc - à adapter selon la localisation)
  const defaultCenter = [31.7917, -7.0926];
  const defaultZoom = 6;
  
  // Gestion des événements sur chaque parcelle
  const onEachParcelle = (feature, layer) => {
    // Popup avec les informations de la parcelle
    const popupContent = `
      <div class="parcelle-popup">
        <h4>${feature.properties?.nom || 'Parcelle'}</h4>
        <p><strong>Surface:</strong> ${feature.properties?.surface || 'N/A'} ha</p>
        <p><strong>Culture:</strong> ${feature.properties?.culture || 'N/A'}</p>
        <p><strong>État:</strong> <span class="etat-${feature.properties?.etat}">${feature.properties?.etat || 'N/A'}</span></p>
      </div>
    `;
    
    layer.bindPopup(popupContent);
    
    // Événements de survol
    layer.on({
      mouseover: (e) => {
        const layer = e.target;
        layer.setStyle(highlightStyle);
        layer.bringToFront();
      },
      mouseout: (e) => {
        if (geoJsonRef.current) {
          geoJsonRef.current.resetStyle(e.target);
        }
      },
      click: () => {
        if (onParcelleClick) {
          onParcelleClick(feature.properties);
        }
      },
    });
  };
  
  return (
    <div className="map-container">
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        className="leaflet-map"
        ref={setMap}
      >
        {/* Couche de base - OpenStreetMap */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Couche satellite optionnelle */}
        {/* 
        <TileLayer
          attribution='&copy; Esri'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        />
        */}
        
        {/* Affichage des parcelles */}
        {parcelles && parcelles.features?.length > 0 && (
          <>
            <GeoJSON
              ref={geoJsonRef}
              data={parcelles}
              style={parcelleStyle}
              onEachFeature={onEachParcelle}
            />
            <FitBounds geoJsonData={parcelles} />
          </>
        )}
      </MapContainer>
      
      {/* Légende */}
      <div className="map-legend">
        <h4>État des parcelles</h4>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#22c55e' }}></span>
          <span>Excellent</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#84cc16' }}></span>
          <span>Bon</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#eab308' }}></span>
          <span>Moyen</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f97316' }}></span>
          <span>Attention</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ef4444' }}></span>
          <span>Critique</span>
        </div>
      </div>
    </div>
  );
}

export default MapView;
