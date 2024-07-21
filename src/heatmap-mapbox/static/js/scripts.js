if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('static/js/service-worker.js')
    .then((registration) => {
        console.log('Service Worker registered with scope:', registration.scope);
    }).catch((error) => {
        console.log('Service Worker registration failed:', error);
    });
}

mapboxgl.accessToken = '{{ mapbox_access_token }}';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v11',
    center: [32.5, 0.35],
    zoom: 2,
    projection: 'mercator' // start with the mercator projection
});

async function fetchData() {
    const response = await fetch('http://127.0.0.1:5000/heatmap-data?lat_north=90&lat_south=-90&lon_east=180&lon_west=-180');
    const data = await response.json();
    return data;
}

async function addHeatmapLayer() {
    const data = await fetchData();

    if (map.getSource('air-quality')) {
        map.getSource('air-quality').setData(data);
    } else {
        map.addSource('air-quality', {
            type: 'geojson',
            data: data
        });

        map.addLayer({
            id: 'air-quality-heat',
            type: 'heatmap',
            source: 'air-quality',
            maxzoom: 12,
            paint: {
                'heatmap-weight': ['interpolate', ['linear'], ['get', 'pm25_level'], 0, 0, 5, 1],
                'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 1, 12, 1],
                'heatmap-color': [
                    'interpolate',
                    ['linear'],
                    ['heatmap-density'],
                    0, 'rgba(0, 255, 0, 0)',
                    0.2, 'rgba(0, 255, 0, 0.5)',
                    0.4, 'rgba(255, 255, 0, 0.5)',
                    0.6, 'rgba(255, 165, 0, 0.5)',
                    0.8, 'rgba(255, 0, 0, 0.5)',
                    1, 'rgba(128, 0, 128, 0.5)',
                    1.2, 'rgba(128, 0, 0, 0.5)'
                ],
                'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 12, 20],
                'heatmap-opacity': 0.5
            }
        });

        map.addLayer({
            id: 'air-quality-square',
            type: 'fill',
            source: 'air-quality',
            minzoom: 2,
            paint: {
                'fill-color': [
                    'step',
                    ['get', 'pm25_level'],
                    'rgba(0, 255, 0, 0.5)', 1,
                    'rgba(255, 255, 0, 0.5)', 2,
                    'rgba(255, 165, 0, 0.5)', 3,
                    'rgba(255, 0, 0, 0.5)', 4,
                    'rgba(128, 0, 128, 0.5)', 5,
                    'rgba(128, 0, 0, 0.5)'
                ],
                'fill-opacity': 0.5,
                'fill-outline-color': 'rgba(255, 255, 255, 0.5)'
            }
        });
    }
}

map.on('load', () => {
    addHeatmapLayer();
});

map.on('style.load', () => {
    addHeatmapLayer();
});

document.getElementById('toggleProjection').addEventListener('click', () => {
    const currentProjection = map.getProjection();
    if (currentProjection.name === 'mercator') {
        map.setProjection('globe');
        document.getElementById('toggleProjection').innerText = 'Switch to Flat Map';
    } else {
        map.setProjection('mercator');
        document.getElementById('toggleProjection').innerText = 'Switch to Globe View';
    }
});

document.getElementById('darkMode').addEventListener('click', () => {
    map.setStyle('mapbox://styles/mapbox/dark-v11');
});

document.getElementById('lightMode').addEventListener('click', () => {
    map.setStyle('mapbox://styles/mapbox/light-v11');
});

document.getElementById('streetMode').addEventListener('click', () => {
    map.setStyle('mapbox://styles/mapbox/streets-v11');
});

document.getElementById('satelliteMode').addEventListener('click', () => {
    map.setStyle('mapbox://styles/mapbox/satellite-v9');
});

document.getElementById('refreshMap').addEventListener('click', () => {
    addHeatmapLayer();
});

document.getElementById('zoomIn').addEventListener('click', () => {
    map.zoomIn();
});

document.getElementById('zoomOut').addEventListener('click', () => {
    map.zoomOut();
});