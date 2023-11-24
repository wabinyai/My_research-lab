import React, { useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-geosearch/dist/geosearch.css';
import { OpenStreetMapProvider, GeoSearchControl } from 'leaflet-geosearch';

const App = () => {
  const [map, setMap] = useState(null);

  const initMap = () => {
    const mymap = L.map('map').setView([0, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(mymap);

    const provider = new OpenStreetMapProvider();
    const searchControl = new GeoSearchControl({
      provider: provider,
      style: 'bar',
      autoComplete: true,
      autoCompleteDelay: 250
    });

    mymap.addControl(searchControl);

    searchControl.on('results', function (data) {
      const { x, y } = data.results[0].location;
      fetch('/get_pm25_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude: y, longitude: x }),
      })
      .then(response => response.json())
      .then(data => {
        const { latitude, longitude, pm2_5 } = data;
        const marker = L.marker([latitude, longitude]).addTo(mymap);
        marker.bindPopup(`PM2.5: ${pm2_5}`).openPopup();
      })
      .catch(error => console.error('Error:', error));
    });

    setMap(mymap);
  };

  if (!map) {
    initMap();
  }

  return null;
};

export default App;
