// SatQuery AI – Simplified GIS Frontend

// ==== Global State ====
let map; // Leaflet map instance
let imageOverlay = null; // Current GeoTIFF overlay
let currentLayer = null; // Metadata of selected layer (dataset)
let layers = []; // Array of dataset objects
let pixelMarker = null; // Crosshair marker for pixel inspector
let selectedPixel = null; // Currently inspected pixel data
let basemapLayer = null; // Basemap layer reference
let drawnItems = null; // LayerGroup for drawn features
let vqaEvidenceLayer = null; // LayerGroup for VQA grounding evidence
let currentAOI = null; // Current Area of Interest

// ==== Initialization ====
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  setupEventListeners();
  updateNoDataState();
});

function initMap() {
  const emptyTileUrl = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==';
  const emptyTile = L.tileLayer(emptyTileUrl, { attribution: '' });

  basemapLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
  });

  basemapLayer.on('tileerror', function(error, tile) {
      basemapLayer.setOpacity(0);
      document.getElementById('basemap-toggle').checked = false;
      document.getElementById('basemap-toggle').disabled = true;
  });

  map = L.map('map', {
    center: [0, 0],
    zoom: 2,
    zoomControl: false,
    layers: [emptyTile, basemapLayer]
  });

  drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);
  vqaEvidenceLayer = L.layerGroup().addTo(map);

  const drawControl = new L.Control.Draw({
    position: 'topleft',
    draw: {
      polyline: false,
      circle: false,
      circlemarker: false,
      marker: true,
      rectangle: true,
      polygon: true
    },
    edit: {
      featureGroup: drawnItems,
      edit: false,
      remove: false
    }
  });
  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, function (e) {
      drawnItems.clearLayers();
      const layer = e.layer;
      drawnItems.addLayer(layer);
      
        const geojson = layer.toGeoJSON();
        let area_m2 = null;
        let area_km2 = null;
        
        let nw, se, west, east, north, south;
        if (e.layerType === 'marker') {
            const ll = layer.getLatLng();
            west = ll.lng; east = ll.lng;
            south = ll.lat; north = ll.lat;
        } else {
            const b = layer.getBounds();
            nw = b.getNorthWest().wrap();
            se = b.getSouthEast().wrap();
            west = nw.lng;
            east = se.lng;
            if (west > east) {
                west = b.getWest();
                east = b.getEast();
            }
            south = b.getSouth();
            north = b.getNorth();
            
            try {
                let latlngs = layer.getLatLngs();
                const ring = (latlngs.length > 0 && Array.isArray(latlngs[0])) ? latlngs[0] : latlngs;
                if (L.GeometryUtil && L.GeometryUtil.geodesicArea) {
                    area_m2 = L.GeometryUtil.geodesicArea(ring);
                    area_km2 = area_m2 / 1000000;
                }
            } catch(err) {
                console.warn("Area calculation error", err);
            }
        }

        currentAOI = { 
            geometry_type: e.layerType === 'marker' ? 'Point' : (e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon'),
            geometry: geojson.geometry,
            bbox: { west, south, east, north },
            area_m2: area_m2,
            area_km2: area_km2,
            
            // Legacy attributes to preserve existing UI compatibility
            type: e.layerType === 'marker' ? 'Point' : (e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon'),
            geojson: geojson
        };
        
        if (e.layerType === 'marker') {
            const ll = layer.getLatLng();
            currentAOI.lat = ll.lat;
            currentAOI.lng = ll.lng;
        } else {
            currentAOI.bounds = layer.getBounds();
            currentAOI.area = area_m2;
        console.log('TEMPORARY AOI LOG for verification:', { geometry_type: currentAOI.geometry_type, geometry: currentAOI.geometry, bbox: currentAOI.bbox, area_m2: currentAOI.area_m2, area_km2: currentAOI.area_km2 });
        }
      updateAOIPanel();
  });

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  map.on('mousemove', (e) => {
    updateStatusBarCoords(e.latlng);
  });
  map.on('zoomend', () => {
    updateStatusBar();
  });
  map.on('click', handleMapClick);
}

// ==== UI Helpers ====
function updateAOIPanel() {
    const noSel = document.getElementById('aoi-no-selection');
    const details = document.getElementById('aoi-details');
    
    if (!currentAOI) {
        if(noSel) noSel.style.display = 'block';
        if(details) details.style.display = 'none';
        return;
    }
    
    if(noSel) noSel.style.display = 'none';
    if(details) details.style.display = 'block';
    
    document.getElementById('aoi-type').textContent = currentAOI.type;
    
    document.getElementById('aoi-point-group').style.display = 'none';
    document.getElementById('aoi-bbox-group').style.display = 'none';
    document.getElementById('aoi-area-group').style.display = 'none';
    
    if (currentAOI.type === 'Point') {
        document.getElementById('aoi-point-group').style.display = 'flex';
        document.getElementById('aoi-coords').textContent = `Latitude: ${currentAOI.lat.toFixed(6)}°\nLongitude: ${currentAOI.lng.toFixed(6)}°`;
    } else {
        document.getElementById('aoi-bbox-group').style.display = 'flex';
        const b = currentAOI.bounds;
        document.getElementById('aoi-bbox').textContent = `North: ${b.getNorth().toFixed(6)}°\nSouth: ${b.getSouth().toFixed(6)}°\nEast: ${b.getEast().toFixed(6)}°\nWest: ${b.getWest().toFixed(6)}°`;
        
        if (currentAOI.area) {
            document.getElementById('aoi-area-group').style.display = 'flex';
            let areaStr = '';
            if (currentAOI.area > 1000000) {
                areaStr = (currentAOI.area / 1000000).toFixed(2) + ' km²';
            } else {
                areaStr = currentAOI.area.toFixed(2) + ' m²';
            }
            document.getElementById('aoi-area').textContent = areaStr;
        }
    }
}

function updateNoDataState() {
  const noDataMsg = document.getElementById('no-data-msg');
  if (layers.length === 0) {
    noDataMsg.style.display = 'block';
  } else {
    noDataMsg.style.display = 'none';
  }
}

function addLayerToList(dataset) {
  let targetList;
  if (dataset.is_analysis) {
      targetList = document.getElementById('list-analysis');
      document.getElementById('group-analysis').style.display = 'block';
      document.getElementById('group-stac').style.display = 'block';
  } else {
      targetList = document.getElementById('list-uploaded');
      document.getElementById('group-uploaded').style.display = 'block';
  }

  const li = document.createElement('li');
  li.dataset.id = dataset.id;
  li.style.cursor = 'pointer';
  li.style.display = 'flex';
  li.style.flexDirection = 'column';
  li.style.paddingBottom = '8px';
  
  const header = document.createElement('div');
  header.style.display = 'flex';
  header.style.alignItems = 'center';
  header.style.gap = '8px';
  
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = true;
  checkbox.disabled = true;

  const nameSpan = document.createElement('span');
  nameSpan.innerHTML = dataset.name;
  nameSpan.style.fontWeight = '600';
  
  const descSpan = document.createElement('span');
  descSpan.style.color = 'var(--muted)';
  descSpan.style.fontSize = '12px';
  descSpan.style.marginLeft = 'auto'; // push to the right side
  
  if (dataset.is_analysis) {
      descSpan.innerHTML = 'NDVI Analysis';
  } else {
      descSpan.innerHTML = `Sentinel-2 &middot; Multispectral`;
  }
  
  header.appendChild(checkbox);
  header.appendChild(nameSpan);
  header.appendChild(descSpan);
  li.appendChild(header);
  
  if (dataset.is_stac) {
      const tree = document.createElement('div');
      tree.style.marginLeft = '24px';
      tree.style.marginTop = '4px';
      tree.style.color = 'var(--text)';
      tree.style.fontSize = '12px';
      tree.style.fontFamily = 'monospace';
      
      dataset.bands.forEach((b, idx) => {
          const isLast = idx === dataset.bands.length - 1;
          const prefix = isLast ? '└── ' : '├── ';
          const node = document.createElement('div');
          node.textContent = `${prefix}${b.id}`;
          tree.appendChild(node);
      });
      li.appendChild(tree);
  }

  li.addEventListener('click', () => {
    selectLayer(dataset.id);
  });

  targetList.appendChild(li);
}

function clearLayerList() {
  document.getElementById('list-uploaded').innerHTML = '';
  document.getElementById('list-stac').innerHTML = '';
  document.getElementById('list-analysis').innerHTML = '';
  
  document.getElementById('group-uploaded').style.display = 'none';
  document.getElementById('group-stac').style.display = 'none';
  document.getElementById('group-analysis').style.display = 'none';
}

function selectLayer(layerId) {
  const layer = layers.find(l => l.id === layerId);
  if (!layer) return;
  currentLayer = layer;
  
  const vqaLabel = document.getElementById('vqa-selected-image-panel');
  if (vqaLabel) vqaLabel.textContent = layer.name;

  // Update UI (highlight selected item and sync checkboxes)
  document.querySelectorAll('.layer-list li').forEach(li => {
    const cb = li.querySelector('input[type="checkbox"]');
    if (li.dataset.id === layerId) {
      li.classList.add('selected');
      if (cb) cb.checked = true;
    } else {
      li.classList.remove('selected');
      if (cb && li.dataset.id) cb.checked = false; // Only uncheck dataset layers, preserve basemap if it were in this list
    }
  });
  
  // Populate dropdowns
  const bandSelect = document.getElementById('layer-band');
  const redSelect = document.getElementById('layer-red');
  const greenSelect = document.getElementById('layer-green');
  const blueSelect = document.getElementById('layer-blue');
  
  [bandSelect, redSelect, greenSelect, blueSelect].forEach(sel => {
      sel.innerHTML = '';
      layer.bands.forEach(b => {
          const opt = document.createElement('option');
          opt.value = b.id;
          opt.textContent = `${b.id} — ${b.description}`;
          sel.appendChild(opt);
      });
  });
  
  const bandIds = layer.bands.map(b => b.id);
  const renderMode = document.getElementById('render-mode');
  const singleControls = document.getElementById('single-band-controls');
  const rgbControls = document.getElementById('rgb-controls');
  
  const rgbOption = renderMode.querySelector('option[value="rgb"]');
  const renderModeGroup = document.getElementById('render-mode-group');
  
  if (layer.is_stac) {
      if (renderModeGroup) renderModeGroup.style.display = 'none';
      bandSelect.value = "True Color";
      singleControls.style.display = 'block';
      rgbControls.style.display = 'block';
      redSelect.value = "B04";
      greenSelect.value = "B03";
      blueSelect.value = "B02";
  } else if (layer.bands.length < 3) {
      if (renderModeGroup) renderModeGroup.style.display = 'block';
      if (rgbOption) rgbOption.style.display = 'none';
      renderMode.value = "single";
      bandSelect.value = layer.bands[0].id;
      singleControls.style.display = 'block';
      rgbControls.style.display = 'none';
  } else {
      if (renderModeGroup) renderModeGroup.style.display = 'block';
      if (rgbOption) rgbOption.style.display = '';
      if (bandIds.includes("B04") && bandIds.includes("B03") && bandIds.includes("B02")) {
          renderMode.value = "rgb";
          redSelect.value = "B04";
          greenSelect.value = "B03";
          blueSelect.value = "B02";
          singleControls.style.display = 'none';
          rgbControls.style.display = 'block';
      } else {
          renderMode.value = "single";
          bandSelect.value = layer.bands[0].id;
          singleControls.style.display = 'block';
          rgbControls.style.display = 'none';
      }
  }

  document.getElementById('layer-opacity').value = "100";
  
  const vminInput = document.getElementById('vis-min');
  const vmaxInput = document.getElementById('vis-max');
  const genericVis = document.getElementById('generic-vis-controls');
  const ndviVis = document.getElementById('ndvi-vis-controls');
  
  if (layer.is_analysis && layer.analysis_data && layer.analysis_data.analysis === 'NDVI') {
      if (genericVis) genericVis.style.display = 'none';
      if (ndviVis) ndviVis.style.display = 'block';
      
      const vis = layer.vis_params || { colormap: 'ndvi', vmin: -1.0, vmax: 1.0, opacity: 100 };
      document.getElementById('ndvi-colormap').value = vis.colormap;
      document.getElementById('ndvi-vis-min').value = vis.vmin;
      document.getElementById('ndvi-vis-max').value = vis.vmax;
      document.getElementById('ndvi-opacity').value = vis.opacity;
      const opVal = document.getElementById('ndvi-opacity-val');
      if (opVal) opVal.textContent = `${vis.opacity}%`;
  } else {
      if (genericVis) genericVis.style.display = 'block';
      if (ndviVis) ndviVis.style.display = 'none';
      
      if (layer.is_analysis) {
          vminInput.value = "";
          vmaxInput.value = "";
          vminInput.disabled = true;
          vmaxInput.disabled = true;
      } else {
          vminInput.disabled = false;
          vmaxInput.disabled = false;
          
          if (layer.is_stac) {
              vminInput.value = "";
              vmaxInput.value = "";
          } else {
              const firstMeta = layer.bands[0].metadata;
              vminInput.value = firstMeta.p2 !== undefined ? firstMeta.p2.toFixed(2) : "";
              vmaxInput.value = firstMeta.p98 !== undefined ? firstMeta.p98.toFixed(2) : "";
          }
      }
  }

  updateMapOverlay();

  // Reset pixel inspector
  document.getElementById('pixel-inspector-section').style.display = 'none';
  if (pixelMarker) {
    map.removeLayer(pixelMarker);
    pixelMarker = null;
  }
  selectedPixel = null;
  
  populateInspector(layer);
  updateStatusBar();
}

function updateMapOverlay() {
  if (!currentLayer) return;
  updateVqaUI();
  
  let opacity = 1.0;
  if (currentLayer.is_analysis && currentLayer.analysis_data.analysis === 'NDVI') {
      opacity = parseInt(document.getElementById('ndvi-opacity').value) / 100.0;
  } else {
      opacity = parseInt(document.getElementById('layer-opacity').value) / 100.0;
  }
  
  const renderMode = document.getElementById('render-mode').value;
  
  let url = `http://127.0.0.1:8000/api/v1/datasets/${currentLayer.id}/preview`;
  

  if (currentLayer.is_analysis) {
      if (currentLayer.analysis_data.analysis === 'NDVI') {
          const colormap = document.getElementById('ndvi-colormap').value;
          const vmin = document.getElementById('ndvi-vis-min').value;
          const vmax = document.getElementById('ndvi-vis-max').value;
          let fixedMax = parseFloat(vmax);
          let fixedMin = parseFloat(vmin);
          if (fixedMin >= fixedMax) fixedMax = fixedMin + 0.1;
          
          const parts = currentLayer.preview_url.split('/');
          const resultId = parts[parts.length - 2];
          
          url = `http://127.0.0.1:8000/api/v1/analysis/render?result_id=${resultId}&colormap=${colormap}&vmin=${fixedMin}&vmax=${fixedMax}`;
      } else {
          url = currentLayer.preview_url;
      }
  } else {
      const band = document.getElementById('layer-band').value;
      const vmin = document.getElementById('vis-min').value;
      const vmax = document.getElementById('vis-max').value;
      
      let params = [];
      if (vmin !== "" && vmax !== "") {
          params.push(`vmin=${vmin}`);
          params.push(`vmax=${vmax}`);
      }
      const paramStr = params.length > 0 ? `?${params.join('&')}` : '';
      
      if (currentLayer.is_stac) {
          if (band === 'True Color') {
              url = currentLayer.preview_url;
          } else {
              url = `http://127.0.0.1:8000/api/v1/catalog/scene/${currentLayer.id}/band/${band}/preview${paramStr}`;
          }
      } else {
          let paramStrLocal = "?";
          if (renderMode === 'rgb') {
              const r = document.getElementById('layer-red').value;
              const g = document.getElementById('layer-green').value;
              const b = document.getElementById('layer-blue').value;
              paramStrLocal += `red=${r}&green=${g}&blue=${b}`;
          } else {
              paramStrLocal += `band=${band}`;
          }
          if (vmin !== "" && vmax !== "") {
              paramStrLocal += `&vmin=${vmin}&vmax=${vmax}`;
          }
          url += paramStrLocal;
      }
  }
  const bounds = currentLayer.bounds;

  if (imageOverlay) {
    map.removeLayer(imageOverlay);
    imageOverlay = null;
  }
  
  if (bounds && bounds.length === 2) {
    imageOverlay = L.imageOverlay(url, bounds, { opacity: opacity }).addTo(map);
    map.fitBounds(bounds);
  } else {
    const worldBounds = [[-90, -180], [90, 180]];
    imageOverlay = L.imageOverlay(url, worldBounds, { opacity: opacity }).addTo(map);
    map.setView([0, 0], 2);
  }
  
  const set = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? '-';
  };
  const vmin = document.getElementById('vis-min').value;
  const vmax = document.getElementById('vis-max').value;
  set('inspector-vmin', vmin !== "" ? vmin : '-');
  set('inspector-vmax', vmax !== "" ? vmax : '-');
  
  const ndviLegend = document.getElementById('ndvi-legend');
  if (ndviLegend) {
      if (currentLayer.is_analysis && currentLayer.analysis_data.analysis === 'NDVI') {
          ndviLegend.style.display = 'block';
          // Update legend dynamically
          const colormap = document.getElementById('ndvi-colormap').value;
          let vmin = parseFloat(document.getElementById('ndvi-vis-min').value);
          let vmax = parseFloat(document.getElementById('ndvi-vis-max').value);
          if (vmin >= vmax) vmax = vmin + 0.1;
          
          let html = `<div style="font-weight: 600; margin-bottom: 8px;">NDVI</div><div style="display: flex; flex-direction: column; gap: 4px;">`;
          const steps = [
              { label: vmax.toFixed(2), frac: 1.0 },
              { label: (vmin + (vmax - vmin) * 0.75).toFixed(2), frac: 0.75 },
              { label: (vmin + (vmax - vmin) * 0.5).toFixed(2), frac: 0.5 },
              { label: (vmin + (vmax - vmin) * 0.25).toFixed(2), frac: 0.25 },
              { label: vmin.toFixed(2), frac: 0.0 }
          ];
          
          steps.forEach(step => {
              let color = '';
              if (colormap === 'grayscale') {
                  const val = Math.round(step.frac * 255);
                  color = `rgb(${val}, ${val}, ${val})`;
              } else if (colormap === 'inverted') {
                  const val = Math.round((1 - step.frac) * 255);
                  color = `rgb(${val}, ${val}, ${val})`;
              } else {
                  if (step.frac >= 0.5) {
                      const f = (step.frac - 0.5) * 2.0;
                      const r = Math.round(255 + f * (0 - 255));
                      const g = Math.round(255 + f * (104 - 255));
                      const b = Math.round(191 + f * (55 - 191));
                      color = `rgb(${r}, ${g}, ${b})`;
                  } else {
                      const f = step.frac * 2.0;
                      const r = Math.round(165 + f * (255 - 165));
                      const g = Math.round(0 + f * (255 - 0));
                      const b = Math.round(38 + f * (191 - 38));
                      color = `rgb(${r}, ${g}, ${b})`;
                  }
              }
              html += `<div style="display: flex; align-items: center; gap: 8px;"><div style="width: 16px; height: 16px; background: ${color};"></div><span>${step.label}</span></div>`;
          });
          html += `</div>`;
          ndviLegend.innerHTML = html;
      } else {
          ndviLegend.style.display = 'none';
      }
  }
}

function populateInspector(dataset) {
  const meta = dataset.metadata; // use base metadata
  
  const set = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? '-';
  };
  
  const datasetProps = document.getElementById('inspector-dataset-props');
  if (dataset.is_analysis) {
        const stats = dataset.analysis_data.statistics;
        const areaStr = dataset.analysis_data.area ? (dataset.analysis_data.area / 1000000).toFixed(2) + ' km²' : '-';
        datasetProps.innerHTML = `
          <div class="prop-row"><span class="label-text">Analysis</span><span class="value-text" id="inspector-sensor">NDVI</span></div>
          <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;">${dataset.source_layer_name || dataset.scene_info?.scene_id || dataset.analysis_data.scene_id}</span></div>
          <div class="prop-row"><span class="label-text">AOI</span><span class="value-text">${dataset.analysis_data.scope || 'Full Scene'}</span></div>
          <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono">${areaStr}</span></div>
          <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">STATISTICS</div>
          <div class="prop-row"><span class="label-text">Minimum NDVI</span><span class="value-text mono">${stats.min.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Maximum NDVI</span><span class="value-text mono">${stats.max.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Mean NDVI</span><span class="value-text mono">${stats.mean.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Median NDVI</span><span class="value-text mono">${stats.median.toFixed(4)}</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">PIXEL COUNTS</div>
          <div class="prop-row"><span class="label-text">Total pixels</span><span class="value-text mono">${(stats.total_pixel_count || 0).toLocaleString()}</span></div>
          <div class="prop-row"><span class="label-text">Valid pixels</span><span class="value-text mono">${(stats.valid_pixel_count || 0).toLocaleString()}</span></div>
          <div class="prop-row"><span class="label-text">No-data pixels</span><span class="value-text mono">${(stats.nodata_pixel_count || 0).toLocaleString()}</span></div>
        `;
    } else if (dataset.is_stac) {
      datasetProps.innerHTML = `
        <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" id="inspector-sensor">Sentinel-2 L2A</span></div>
        <div class="prop-row"><span class="label-text">Acquisition</span><span class="value-text" id="inspector-acq">${dataset.scene_info.datetime.split('T')[0]}</span></div>
        <div class="prop-row"><span class="label-text">Cloud cover</span><span class="value-text" id="inspector-cloud">${dataset.scene_info.cloud_cover.toFixed(1)}%</span></div>
        <div class="prop-row" style="flex-direction: column; align-items: flex-start; gap: 4px;">
            <span class="label-text">Scene ID</span>
            <span class="value-text mono" style="font-size: 11px; word-break: break-all;" id="inspector-sceneid">${dataset.scene_info.scene_id}</span>
        </div>
        <div class="prop-row" style="flex-direction: column; align-items: flex-start; gap: 4px; margin-top: 8px;">
            <span class="label-text">Available assets</span>
            <span class="value-text mono" style="font-size: 11px; word-break: break-word;" id="inspector-assets">${Object.keys(dataset.scene_info.assets).join(', ')}</span>
        </div>
      `;
  } else {
      datasetProps.innerHTML = `
        <div class="prop-row"><span class="label-text">Sensor</span><span class="value-text" id="inspector-sensor">-</span></div>
        <div class="prop-row"><span class="label-text">Band</span><span class="value-text" id="inspector-band">-</span></div>
        <div class="prop-row"><span class="label-text">Dimensions</span><span class="value-text" id="inspector-dim">-</span></div>
        <div class="prop-row"><span class="label-text">Data type</span><span class="value-text mono" id="inspector-dtype">-</span></div>
      `;
      set('inspector-sensor', 'Sentinel-2');
      set('inspector-band', dataset.bands.length === 1 ? `Band ${dataset.bands[0].id.replace('B0', '').replace('B', '')} — ${dataset.bands[0].description}` : `${dataset.bands.length} bands`);
      set('inspector-dim', `${meta.width || '-'} × ${meta.height || '-'}`);
      set('inspector-dtype', meta.dtype || '-');
  }

  set('inspector-name', dataset.name || '-');
  set('inspector-source-crs', meta.source_crs || meta.crs || '-');
  set('inspector-display-crs', 'EPSG:3857');
  set('inspector-coord-crs', 'EPSG:4326');
  set('inspector-res', meta.resolution ? `${Math.abs(meta.resolution).toFixed(0)} m` : '-');
  
  if (dataset.bounds) {
      set('inspector-bounds', `[${dataset.bounds[0][0].toFixed(4)}, ${dataset.bounds[0][1].toFixed(4)}] to [${dataset.bounds[1][0].toFixed(4)}, ${dataset.bounds[1][1].toFixed(4)}]`);
  } else {
      set('inspector-bounds', '-');
  }
  
  set('inspector-driver', meta.driver || '-');
  set('inspector-status', dataset.is_stac ? `STAC reference` : `Loaded successfully`);
}

function updateStatusBarCoords(latlng) {
  const statusBar = document.getElementById('status-bar');
  if (!currentLayer) return;
  const zoom = map.getZoom();
  let text = `CRS: ${currentLayer.metadata.crs || 'EPSG:4326'} | Zoom: ${zoom} | Cursor: ${latlng.lat.toFixed(4)}° N, ${latlng.lng.toFixed(4)}° E`;
  const res = currentLayer.metadata.resolution_x || currentLayer.metadata.resolution;
  if (res) text += ` | Resolution: ${Math.abs(res).toFixed(0)} m`;
  text += ` | Selected: ${currentLayer.name}`;
  if (selectedPixel) {
      text += ` | Pixel: row ${selectedPixel.row}, col ${selectedPixel.column}`;
  }
  statusBar.textContent = text;
}

function updateStatusBar() {
  const statusBar = document.getElementById('status-bar');
  if (!currentLayer) {
    statusBar.textContent = 'Ready';
    return;
  }
  const zoom = map.getZoom();
  const center = map.getCenter();
  let text = `CRS: ${currentLayer.metadata.crs || 'EPSG:4326'} | Zoom: ${zoom} | Center: ${center.lat.toFixed(4)}° N, ${center.lng.toFixed(4)}° E`;
  const res = currentLayer.metadata.resolution_x || currentLayer.metadata.resolution;
  if (res) text += ` | Resolution: ${Math.abs(res).toFixed(0)} m`;
  text += ` | Selected: ${currentLayer.name}`;
  if (selectedPixel) {
      text += ` | Pixel: row ${selectedPixel.row}, col ${selectedPixel.column}`;
  }
  statusBar.textContent = text;
}

async function handleMapClick(e) {
  if (!currentLayer) return;
  
  const section = document.getElementById('pixel-inspector-section');
  const details = document.getElementById('pixel-details');
  const errorSection = document.getElementById('pixel-error-section');
  
  section.style.display = 'block';
  details.style.display = 'block';
  errorSection.style.display = 'none';
  document.getElementById('pixel-coords').textContent = 'Loading...';
  document.getElementById('pixel-rc').textContent = '-';
  document.getElementById('pixel-band-values-container').innerHTML = '';
  document.getElementById('pixel-dtype').textContent = '-';
  document.getElementById('pixel-res').textContent = '-';
  
  if (pixelMarker) map.removeLayer(pixelMarker);
  pixelMarker = L.circleMarker(e.latlng, {
      radius: 5,
      color: 'var(--accent-cyan)',
      weight: 2,
      fillOpacity: 0
  }).addTo(map);
  
  try {
      const resp = await fetch(`http://127.0.0.1:8000/api/v1/datasets/${currentLayer.id}/pixel?lat=${e.latlng.lat}&lon=${e.latlng.lng}`);
      if (!resp.ok) throw new Error('Failed to fetch pixel');
      const data = await resp.json();
      
      if (data.status === 'outside') {
          details.style.display = 'none';
          errorSection.style.display = 'block';
          selectedPixel = null;
      } else {
          details.style.display = 'block';
          errorSection.style.display = 'none';
          
          const latDir = data.latitude >= 0 ? 'N' : 'S';
          const lonDir = data.longitude >= 0 ? 'E' : 'W';
          
          document.getElementById('pixel-coords').textContent = `${Math.abs(data.latitude).toFixed(4)}° ${latDir}\n${Math.abs(data.longitude).toFixed(4)}° ${lonDir}`;
          document.getElementById('pixel-rc').textContent = `Row ${data.row}\nColumn ${data.column}`;
          document.getElementById('pixel-dtype').textContent = data.dtype || currentLayer.metadata.dtype;
          document.getElementById('pixel-res').textContent = `${Math.abs(data.resolution_x).toFixed(0)} m`;
          
          // Populate dynamic values list
          const valuesContainer = document.getElementById('pixel-band-values-container');
          valuesContainer.innerHTML = '';
          
          if (data.values.length === 1) {
              const v = data.values[0];
              const bandName = `Band ${v.band.replace('B0', '').replace('B', '')} — ${v.description}`;
              
              valuesContainer.innerHTML = `
                <div class="prop-col" style="margin-bottom: 12px;">
                   <span class="label-text">Band</span>
                   <span class="value-text" id="pixel-band">${bandName}</span>
                </div>
                <div class="prop-col" style="margin-bottom: 12px;">
                   <span class="label-text">Value</span>
                   <span class="value-text mono" id="pixel-value" style="font-weight:600; color: var(--accent);">${v.error ? 'Error' : v.value}</span>
                </div>
              `;
          } else {
              valuesContainer.innerHTML = `<div class="prop-col" style="margin-bottom: 12px;"><span class="label-text">Values</span><div class="multi-values"></div></div>`;
              const dd = valuesContainer.querySelector('.multi-values');
              data.values.forEach(v => {
                  const div = document.createElement('div');
                  div.style.marginBottom = '6px';
                  const title = document.createElement('div');
                  title.textContent = `${v.band} — ${v.description}`;
                  title.className = 'label-text';
                  const val = document.createElement('div');
                  val.textContent = v.error ? 'Error' : v.value;
                  val.className = 'value-text mono';
                  val.style.fontWeight = '600';
                  val.style.color = 'var(--accent)';
                  div.appendChild(title);
                  div.appendChild(val);
                  dd.appendChild(div);
              });
          }
          
          selectedPixel = data;
      }
      
      updateStatusBarCoords(e.latlng);
      
  } catch (err) {
      console.error(err);
      details.style.display = 'none';
      errorSection.style.display = 'block';
      selectedPixel = null;
  }
}

// ==== Event Listeners ====
function setupEventListeners() {
  document.getElementById('btn-clear-aoi').addEventListener('click', () => {
      drawnItems.clearLayers();
      currentAOI = null;
      updateAOIPanel();
  });

  document.getElementById('btn-add-data').addEventListener('click', () => {
    document.getElementById('geotiff-upload').click();
  });
  
  document.getElementById('geotiff-upload').addEventListener('change', async (e) => {
    const fileInput = e.target;
    if (!fileInput.files.length) return;
    
    document.getElementById('header-status').textContent = 'Uploading...';
    
    const form = new FormData();
    for (let i=0; i<fileInput.files.length; i++) {
        form.append('files', fileInput.files[i]);
    }
    
    try {
      const resp = await fetch('http://127.0.0.1:8000/api/v1/images/upload', {
        method: 'POST',
        body: form
      });
      const data = await resp.json();
      if (!resp.ok) {
          throw new Error(data.detail || 'Upload failed');
      }
      
      const datasetMeta = {
        id: data.dataset_id || data.id,
        name: data.name || data.filename,
        bounds: data.bounds,
        bands: data.bands || [],
        metadata: data.metadata || (data.bands && data.bands.length > 0 ? data.bands[0].metadata : {})
      };

      const existingIndex = layers.findIndex(l => l.id === datasetMeta.id);
      if (existingIndex >= 0) {
          layers[existingIndex] = datasetMeta;
      } else {
          layers.push(datasetMeta);
      }
      clearLayerList();
      layers.forEach(addLayerToList);
      updateNoDataState();
      
      selectLayer(datasetMeta.id);
      document.getElementById('header-status').textContent = `Dataset loaded: ${datasetMeta.name}`;
      fileInput.value = '';
    } catch (err) {
      console.error(err);
      alert(`Error uploading dataset:\n${err.message}`);
      document.getElementById('header-status').textContent = 'Upload failed';
      fileInput.value = '';
    }
  });

  // Render controls
  document.getElementById('render-mode').addEventListener('change', (e) => {
      const isRgb = e.target.value === 'rgb';
      document.getElementById('single-band-controls').style.display = isRgb ? 'none' : 'block';
      document.getElementById('rgb-controls').style.display = isRgb ? 'block' : 'none';
      updateMapOverlay();
  });

  const selectRedraw = () => {
      if (currentLayer && currentLayer.is_stac) {
          const band = document.getElementById('layer-band').value;
          document.getElementById('rgb-controls').style.display = (band === 'True Color') ? 'block' : 'none';
      }
      updateMapOverlay();
  };
  document.getElementById('layer-band').addEventListener('change', selectRedraw);
  document.getElementById('layer-red').addEventListener('change', selectRedraw);
  document.getElementById('layer-green').addEventListener('change', selectRedraw);
  document.getElementById('layer-blue').addEventListener('change', selectRedraw);

  let debounceTimer;
  const updateVis = () => {
    if (!currentLayer) return;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        updateMapOverlay();
    }, 500); 
  };

  document.getElementById('vis-min').addEventListener('input', updateVis);
  document.getElementById('vis-max').addEventListener('input', updateVis);
  
  document.getElementById('layer-opacity').addEventListener('input', (e) => {
    if (imageOverlay) {
        imageOverlay.setOpacity(parseInt(e.target.value) / 100.0);
    }
    const el = document.getElementById('inspector-opo');
    if (el) el.textContent = `${e.target.value}%`;
  });
  
  const ndviColormapEl = document.getElementById('ndvi-colormap');
  if (ndviColormapEl) {
      const saveAndUpdate = () => {
          if (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data.analysis === 'NDVI') {
              currentLayer.vis_params = currentLayer.vis_params || {};
              currentLayer.vis_params.colormap = document.getElementById('ndvi-colormap').value;
              let vmin = parseFloat(document.getElementById('ndvi-vis-min').value);
              let vmax = parseFloat(document.getElementById('ndvi-vis-max').value);
              
              if (vmin >= vmax) {
                  vmax = vmin + 0.1;
                  document.getElementById('ndvi-vis-max').value = vmax.toFixed(1);
              }
              
              currentLayer.vis_params.vmin = vmin;
              currentLayer.vis_params.vmax = vmax;
          }
          updateVis();
      };
      
      ndviColormapEl.addEventListener('change', saveAndUpdate);
      document.getElementById('ndvi-vis-min').addEventListener('input', saveAndUpdate);
      document.getElementById('ndvi-vis-max').addEventListener('input', saveAndUpdate);
      
      document.getElementById('ndvi-opacity').addEventListener('input', (e) => {
          if (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data.analysis === 'NDVI') {
              currentLayer.vis_params = currentLayer.vis_params || {};
              currentLayer.vis_params.opacity = parseInt(e.target.value);
              if (imageOverlay) {
                  imageOverlay.setOpacity(currentLayer.vis_params.opacity / 100.0);
              }
          }
          const el = document.getElementById('ndvi-opacity-val');
          if (el) el.textContent = `${e.target.value}%`;
      });
  }
  
  const btnExport = document.getElementById('btn-export-geotiff');
  const btnReport = document.getElementById('btn-generate-report');
  
  if (btnExport) btnExport.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      alert('Export GeoTIFF functionality is not yet implemented.');
  });
  if (btnReport) btnReport.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();
      try {
        const payload = {
            layer: currentLayer ? {
                name: currentLayer.name,
                id: currentLayer.id,
                stac_properties: currentLayer.stac_properties || {}
            } : null,
            aoi: currentAOI ? {
                type: currentAOI.geometry_type || currentAOI.type,
                area: currentAOI.area_m2 || currentAOI.area,
                bounds: {
                    north: currentAOI.bounds ? currentAOI.bounds.getNorth() : currentAOI.bbox.north,
                    south: currentAOI.bounds ? currentAOI.bounds.getSouth() : currentAOI.bbox.south,
                    east: currentAOI.bounds ? currentAOI.bounds.getEast() : currentAOI.bbox.east,
                    west: currentAOI.bounds ? currentAOI.bounds.getWest() : currentAOI.bbox.west
                }
            } : null,
            ndvi: (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data) ? {
                ...currentLayer.analysis_data,
                source_crs: currentLayer.metadata?.source_crs || currentLayer.metadata?.crs || '-',
                display_crs: 'EPSG:3857',
                resolution: currentLayer.metadata?.resolution ? `${Math.abs(currentLayer.metadata.resolution).toFixed(0)} m` : '-'
            } : null,
            vqa: document.getElementById('vqa-answer').textContent !== '-' && document.getElementById('vqa-answer').textContent !== 'Analyzing satellite image...' ? {
                question: document.getElementById('query-input-panel').value,
                answer: document.getElementById('vqa-answer').textContent,
                confidence_status: document.getElementById('vqa-confidence').textContent,
                execution: {
                    model: 'google/paligemma-3b-ft-rsvqa-hr-224'
                }
            } : null
        };
        
        btnReport.disabled = true;
        btnReport.textContent = "Generating...";
        
        if (imageOverlay && imageOverlay._url) {
            try {
                const imgRes = await fetch(imageOverlay._url);
                const blob = await imgRes.blob();
                payload.image_data = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                });
            } catch (e) {
                console.warn("Could not fetch image data for PDF: ", e);
            }
        }
        
        const res = await fetch('http://127.0.0.1:8000/api/v1/export/pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) throw new Error('Failed to generate report');
        
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'satquery_report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        alert("Error exporting PDF: " + e.message);
    } finally {
        btnReport.disabled = false;
        btnReport.textContent = "Export PDF Report";
    }
});

  const tabs = ['data', 'analysis', 'query', 'export', 'settings'];
  tabs.forEach(tab => {
      const navEl = document.getElementById(`nav-${tab}`);
      if (navEl) {
          navEl.addEventListener('click', (e) => {
              tabs.forEach(t => {
                  const nt = document.getElementById(`nav-${t}`);
                  if (nt) {
                      nt.classList.remove('active');
                  }
                  const p = document.getElementById(`${t}-panel`);
                  if (p) p.style.display = 'none';
              });
              navEl.classList.add('active');
              
              const p = document.getElementById(`${tab}-panel`);
              if (p) {
                  p.style.display = (tab === 'data' || tab === 'query') ? 'flex' : 'block';
              }
          });
      }
  });

  
  const projNav = document.getElementById('nav-project');
  if (projNav) projNav.addEventListener('click', () => alert("Project management is not implemented yet."));

  function getVqaContext() {
      if (!currentLayer) return null;
      let image_type = "raster";
      let modality = "optical";
      let representation = "single_band";
      let displayName = currentLayer.name;
      let source = "unknown";
      
      if (currentLayer.is_stac) {
          image_type = "satellite_scene";
          source = "sentinel-2";
          const band = document.getElementById('layer-band').value;
          if (band === "True Color") {
              representation = "rgb";
              displayName = "Sentinel-2 True Color";
          } else {
              representation = "single_band";
              displayName = band;
          }
      } else if (currentLayer.is_analysis) {
          image_type = "analysis";
          modality = "derived";
          source = "satquery_analysis";
          representation = currentLayer.analysis_data.analysis ? currentLayer.analysis_data.analysis.toLowerCase() : "unknown";
          displayName = currentLayer.name;
      } else {
          image_type = "raster";
          modality = "optical";
          source = "uploaded_raster";
          const renderMode = document.getElementById('render-mode') ? document.getElementById('render-mode').value : 'single';
          if (renderMode === 'rgb' || (currentLayer.bands && currentLayer.bands.length >= 3 && renderMode !== 'single')) {
              representation = "rgb";
              displayName = currentLayer.name + " (RGB)";
          } else {
              representation = "single_band";
              displayName = currentLayer.name;
          }
      }
      return { image_type, modality, representation, displayName, source };
  }

  window.updateVqaUI = function() {
      const vqaLabel = document.getElementById('vqa-selected-image-panel');
      if (!vqaLabel) return;
      const ctx = getVqaContext();
      if (!ctx) {
          vqaLabel.textContent = "None";
      } else {
          vqaLabel.textContent = ctx.displayName;
      }
  };

  const btnQueryPanel = document.getElementById('btn-query-panel');
  const qInputPanel = document.getElementById('query-input-panel');
  if (qInputPanel && btnQueryPanel) {
      qInputPanel.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              btnQueryPanel.click();
          }
      });
  }

  if (btnQueryPanel) {
      btnQueryPanel.addEventListener('click', async () => {
          const qInput = document.getElementById('query-input-panel');
          const q = qInput.value.trim();
          
          document.getElementById('header-status').textContent = 'VALIDATING...';
          const ctx = getVqaContext();
          if (!ctx) {
              document.getElementById('header-status').textContent = 'ERROR: No image selected';
              alert("No satellite image selected.");
              return;
          }
          if (ctx.representation !== 'rgb') {
              document.getElementById('header-status').textContent = 'ERROR: Incompatible image';
              alert("VQA currently requires an RGB image. Select Sentinel-2 True Color or upload an RGB image.");
              return;
          }
          if (!q) {
              document.getElementById('header-status').textContent = 'ERROR: Empty question';
              alert("Enter a question about the selected image.");
              return;
          }
          if (q.length > 500) {
              document.getElementById('header-status').textContent = 'ERROR: Question too long';
              alert("Question is too long.");
              return;
          }
          
          document.getElementById('gpu-offline-banner').style.display = 'none';
          
          const historyContainer = document.getElementById('query-history-container');
          document.getElementById('query-history-empty').style.display = 'none';
          
          const historyItem = document.createElement('div');
          historyItem.style.background = 'var(--app-bg)';
          historyItem.style.border = '1px solid var(--border)';
          historyItem.style.borderRadius = 'var(--radius)';
          historyItem.style.padding = '12px';
          
          const qDiv = document.createElement('div');
          qDiv.style.fontWeight = '600';
          qDiv.style.color = 'var(--text)';
          qDiv.style.marginBottom = '8px';
          qDiv.textContent = "Q: " + q;
          
          const aDiv = document.createElement('div');
          aDiv.style.color = 'var(--text-light)';
          aDiv.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> Analyzing satellite image...';
          
          historyItem.appendChild(qDiv);
          historyItem.appendChild(aDiv);
          historyContainer.prepend(historyItem);
          
          const resultSec = document.getElementById('vqa-result-section');
          resultSec.style.display = 'block';
          
          document.getElementById('vqa-answer').textContent = "Analyzing satellite image...";
          document.getElementById('vqa-answer').style.color = "var(--text-light)";
          document.getElementById('vqa-confidence').textContent = "-";
          document.getElementById('vqa-evidence').textContent = "-";
          document.getElementById('vqa-execution').textContent = "-";
          
          btnQueryPanel.disabled = true;
          document.getElementById('header-status').textContent = 'RUNNING...';
          
          let aoiData = null;
        if (currentAOI) {
            aoiData = {
                type: 'bbox',
                shape: currentAOI.geometry_type,
                area: currentAOI.area_m2 || 0,
                north: currentAOI.bbox.north,
                south: currentAOI.bbox.south,
                east: currentAOI.bbox.east,
                west: currentAOI.bbox.west,
                geometry: currentAOI.geometry
            };
        }
        
        try {
            if (vqaEvidenceLayer) vqaEvidenceLayer.clearLayers();
            
            const res = await fetch('http://127.0.0.1:8000/api/v1/vqa/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_id: currentLayer.id,
                    image_type: ctx.image_type,
                    source: ctx.source,
                    modality: ctx.modality,
                    representation: ctx.representation,
                    question: q,
                    mode: 'vqa',
                    aoi: aoiData
                })
            });
              
              const data = await res.json();
              if (!res.ok) {
                  throw new Error(data.detail || `HTTP Error ${res.status}`);
              }
              
              document.getElementById('header-status').textContent = data.execution?.status === 'error' ? 'ERROR' : 'SUCCESS';
              
              const ansText = data.answer || "No answer returned.";
              aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i> ${ansText}</span>`;
              
              const statusDiv = document.createElement('div');
              statusDiv.style.fontSize = '11px';
              statusDiv.style.color = 'var(--text-muted)';
              statusDiv.style.marginTop = '8px';
              statusDiv.textContent = `Provider: ${data.execution?.provider || 'remote'} | Model: ${data.execution?.model || 'unknown'} | Status: ${data.execution?.status || 'success'}`;
              historyItem.appendChild(statusDiv);
              
              document.getElementById('vqa-answer').textContent = ansText;
              document.getElementById('vqa-confidence').textContent = data.confidence_status === 'not_calibrated' ? "Not calibrated" : `${data.confidence}`;
              
              // Handle Evidence
              const evidenceEl = document.getElementById('vqa-evidence');
              if (data.evidence && data.evidence.length > 0) {
                  evidenceEl.innerHTML = '';
                  data.evidence.forEach(ev => {
                      const div = document.createElement('div');
                      div.style.marginBottom = '8px';
                      const scoreStr = ev.confidence !== null && ev.confidence !== undefined 
                          ? `Grounding score: ${ev.confidence.toFixed(2)}` 
                          : '';
                      div.innerHTML = `<strong>${ev.label}</strong><br><span style="font-size: 11px; color: var(--text-secondary);">${scoreStr}</span><br><a href="#" style="font-size:11px;">[Show on map]</a>`;
                      evidenceEl.appendChild(div);
                      
                      const link = div.querySelector('a');
                      link.addEventListener('click', (e) => {
                          e.preventDefault();
                          if (ev.geometry && ev.geometry.coordinate_system === 'wgs84') {
                              if (ev.type === 'bbox' && ev.geometry.coordinates.length === 4) {
                                  const [x1, y1, x2, y2] = ev.geometry.coordinates;
                                  const bounds = [[y1, x1], [y2, x2]];
                                  L.rectangle(bounds, {color: '#f00', weight: 2}).bindPopup(ev.label).addTo(vqaEvidenceLayer);
                              }
                          } else if (ev.geometry && ev.geometry.coordinate_system === 'image_pixel') {
                                if (currentLayer && currentLayer.bounds) {
                                    if (ev.type === 'bbox' && ev.geometry.coordinates.length === 4) {
                                        const [x1, y1, x2, y2] = ev.geometry.coordinates;
                                        const w = 1024;
                                        const h = 1024;
                                        let bounds = currentLayer.bounds;
                                        if (aoiData) {
                                            bounds = [[aoiData.south, aoiData.west], [aoiData.north, aoiData.east]];
                                        }
                                        const s = bounds[0][0], w_ = bounds[0][1], n = bounds[1][0], e_ = bounds[1][1];
                                        const lat1 = n - (y1 / h) * (n - s);
                                        const lon1 = w_ + (x1 / w) * (e_ - w_);
                                        const lat2 = n - (y2 / h) * (n - s);
                                        const lon2 = w_ + (x2 / w) * (e_ - w_);
                                      L.rectangle([[lat1, lon1], [lat2, lon2]], {color: '#f00', weight: 2}).bindPopup(`${ev.label} (${scoreStr})`).addTo(vqaEvidenceLayer);
                                  }
                              } else {
                                  alert("Cannot map pixel coordinates to this image.");
                              }
                          }
                      });
                  });
              } else {
                  evidenceEl.textContent = "No spatial evidence returned.";
              }
              
              const gProvider = data.execution?.grounding?.provider || 'none';
              const gStatus = data.execution?.grounding?.status || 'not_connected';
              document.getElementById('vqa-execution').textContent = `Task: ${data.task}\nModel: ${data.execution?.model || 'None'}\nProvider: ${data.execution?.provider || 'Unknown'}\nStatus: ${data.execution?.status || 'Unknown'}\nGrounding Provider: ${gProvider}\nGrounding Status: ${gStatus}`;
              
          } catch (e) {
              console.error(e);
              document.getElementById('header-status').textContent = 'ERROR';
              document.getElementById('vqa-answer').textContent = "—";
              document.getElementById('vqa-answer').style.color = "var(--text-light)";
              document.getElementById('vqa-confidence').textContent = "Not calibrated";
              document.getElementById('vqa-evidence').textContent = "No spatial evidence returned.";
              
              let errMsg = e.message;
              if (errMsg.includes('<html') || errMsg.includes('ERR_NGROK')) {
                  errMsg = "Remote GPU inference service is currently unavailable.";
                  document.getElementById('gpu-offline-banner').style.display = 'block';
              }
              
              aDiv.innerHTML = `<span style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation" style="margin-right: 6px;"></i> Unable to complete this query.<br><br><span style="font-size: 11px;">Reason:<br>${errMsg}</span></span>`;
              
              document.getElementById('vqa-execution').textContent = `Task: vqa\nModel: google/paligemma-3b-ft-rsvqa-hr-224\nProvider: remote\nStatus: error\n\nMessage:\n${errMsg}`;
          } finally {
              btnQueryPanel.disabled = false;
          }
      });
  }

  // ==== BASEMAP TOGGLE ====
  const basemapToggle = document.getElementById('basemap-toggle');
  if (basemapToggle) {
      basemapToggle.addEventListener('change', (e) => {
          if (e.target.checked) {
              basemapLayer.setOpacity(1);
          } else {
              basemapLayer.setOpacity(0);
          }
      });
  }

  // ==== MAP CONTROLS ====
  const mcZoomIn = document.getElementById('mc-zoom-in');
  if (mcZoomIn) mcZoomIn.addEventListener('click', () => map.zoomIn());

  const mcZoomOut = document.getElementById('mc-zoom-out');
  if (mcZoomOut) mcZoomOut.addEventListener('click', () => map.zoomOut());

  const mcLocate = document.getElementById('mc-locate');
  if (mcLocate) mcLocate.addEventListener('click', () => map.locate({setView: true, maxZoom: 16}));

  const mcFit = document.getElementById('mc-fit');
  if (mcFit) {
      mcFit.addEventListener('click', () => {
          if (currentLayer && currentLayer.bounds) {
              map.fitBounds(currentLayer.bounds);
          }
      });
  }

  const mcLayers = document.getElementById('mc-layers');
  if (mcLayers) {
      mcLayers.addEventListener('click', () => {
          document.getElementById('nav-data').click();
      });
  }

  const mcDraw = document.getElementById('mc-draw');
  if (mcDraw) {
      mcDraw.addEventListener('click', () => {
          if (drawnItems && drawnItems.getLayers().length > 0) {
              drawnItems.clearLayers();
              currentAOI = null;
              updateAOIPanel();
          } else {
              new L.Draw.Rectangle(map, { shapeOptions: { color: 'var(--accent)' } }).enable();
          }
      });
  }

  const mcMeasure = document.getElementById('mc-measure');
  if (mcMeasure) mcMeasure.addEventListener('click', () => alert("Measure tool is not connected yet."));

  const mcPixel = document.getElementById('mc-pixel');
  if (mcPixel) {
      mcPixel.addEventListener('click', () => {
          alert("Click anywhere on the map to inspect pixel values.");
      });
  }

  // ==== STAC SEARCH ====
  const stacCloudCover = document.getElementById('stac-cloud-cover');
  const stacCloudVal = document.getElementById('stac-cloud-val');
  if (stacCloudCover && stacCloudVal) {
      stacCloudCover.addEventListener('input', (e) => {
          stacCloudVal.textContent = e.target.value;
      });
  }

  const btnSearchStac = document.getElementById('btn-search-stac');
  if (btnSearchStac) {
      btnSearchStac.addEventListener('click', async () => {
          

          const btn = btnSearchStac;
          const origHtml = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> Searching satellite catalog...';
          btn.disabled = true;
          
          const feedback = document.getElementById('stac-search-feedback');
          const container = document.getElementById('stac-results-container');
          
          if (feedback) {
              feedback.style.display = 'block';
              feedback.style.color = 'var(--text)';
              feedback.textContent = 'Searching satellite catalog...';
          }
          if (container) container.innerHTML = '';

          try {
              const bounds = map.getBounds();
              
              let minLon = bounds.getWest();
              let maxLon = bounds.getEast();
              const minLat = bounds.getSouth();
              const maxLat = bounds.getNorth();
              
              // Fix CRS transformation problem: Leaflet continuously adds 360 to longitude 
              // as you pan right. We must wrap it back to standard WGS84 [-180, 180].
              if (maxLon - minLon >= 360) {
                  minLon = -180;
                  maxLon = 180;
              } else {
                  minLon = bounds.getSouthWest().wrap().lng;
                  maxLon = bounds.getNorthEast().wrap().lng;
              }
              
              const bbox = [minLon, minLat, maxLon, maxLat];
              
              // Validate STAC requirements
              if (minLon < -180 || maxLon > 180 || minLat < -90 || maxLat > 90) {
                  throw new Error(`Invalid STAC geographic bounding box: [${bbox.join(', ')}]`);
              }
              
              // Date inputs natively provide YYYY-MM-DD
              const startDate = document.getElementById('stac-start-date').value;
              const endDate = document.getElementById('stac-end-date').value;
              const maxCloud = parseFloat(document.getElementById('stac-cloud-cover').value);

              const req = {
                  bbox: bbox,
                  start_date: startDate,
                  end_date: endDate,
                  max_cloud_cover: maxCloud,
                  collection: 'sentinel-2-l2a',
                  limit: 5
              };
              
              console.log("SEARCH REQUEST PAYLOAD", req);

              const resp = await fetch('http://127.0.0.1:8000/api/v1/catalog/search', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify(req)
              });
              
              console.log("SEARCH HTTP STATUS", resp.status);
              
              if (!resp.ok) {
                  const errText = await resp.text();
                  throw new Error(`HTTP ${resp.status} - ${errText}`);
              }
              const data = await resp.json();
              console.log("SEARCH RESPONSE", data);
              
              if (feedback) feedback.style.display = 'none';
              
              if (data.results.length === 0) {
                  if (feedback) {
                      feedback.style.display = 'block';
                      feedback.style.color = 'var(--text)';
                      feedback.textContent = 'No scenes found matching criteria.';
                  }
              } else {
                  // Add title
                  const title = document.createElement('div');
                  title.className = 'section-title';
                  title.textContent = 'SEARCH RESULTS';
                  title.style.marginTop = '8px';
                  container.appendChild(title);
                  
                  data.results.forEach(scene => {
                      const dateStr = scene.datetime.split('T')[0];
                      const div = document.createElement('div');
                      div.style.border = '1px solid var(--border)';
                      div.style.padding = '8px';
                      div.style.borderRadius = 'var(--radius)';
                      div.style.display = 'flex';
                      div.style.flexDirection = 'column';
                      div.style.gap = '8px';
                      
                      const info = document.createElement('div');
                      info.innerHTML = `
                        <div style="font-weight: 600; color: var(--text);">Sentinel-2</div>
                        <div style="color: var(--muted); font-size: 12px;">${dateStr}</div>
                        <div style="color: var(--muted); font-size: 12px;">Cloud cover: ${scene.cloud_cover.toFixed(1)}%</div>
                      `;
                      
                      const actions = document.createElement('div');
                      actions.style.display = 'flex';
                      actions.style.gap = '8px';
                      
                      const btnPreview = document.createElement('button');
                      btnPreview.className = 'btn btn-secondary';
                      btnPreview.style.flex = '1';
                      btnPreview.textContent = 'Preview';
                      btnPreview.onclick = () => alert(`Metadata:\nScene ID: ${scene.scene_id}\nDate: ${scene.datetime}\nClouds: ${scene.cloud_cover.toFixed(1)}%\nAssets: ${Object.keys(scene.assets).length}`);
                      
                      const btnLoad = document.createElement('button');
                      btnLoad.className = 'btn btn-primary';
                      btnLoad.style.flex = '1';
                      btnLoad.textContent = 'Load';
                      btnLoad.onclick = () => {
                          loadStacScene(scene);
                      };
                      
                      actions.appendChild(btnPreview);
                      actions.appendChild(btnLoad);
                      
                      div.appendChild(info);
                      div.appendChild(actions);
                      container.appendChild(div);
                  });
              }
              
          } catch (err) {
              console.error(err);
              if (feedback) {
                  feedback.style.display = 'block';
                  feedback.style.color = '#ff4a4a'; // Error red
                  feedback.textContent = `Satellite catalog search failed: ${err.message}`;
              }
          } finally {
              btn.innerHTML = origHtml;
              btn.disabled = false;
          }
      });
  }
}

async function loadStacScene(scene) {
    try {
        document.getElementById('header-status').textContent = `Loading STAC scene data...`;
        const res = await fetch(`http://127.0.0.1:8000/api/v1/catalog/scene/${scene.scene_id}`);
        if (!res.ok) {
            throw new Error(`HTTP Error: ${res.status}`);
        }
        const data = await res.json();
        
        console.log("SCENE RENDER");
        console.log(`Scene: ${scene.scene_id}`);
        console.log(`Asset: ${data.asset_key}`);
        console.log(`Source CRS: ${data.source_crs}`);
        console.log(`Source dimensions: ${data.source_width} x ${data.source_height}`);
        console.log(`Source bounds: ${JSON.stringify(data.source_bounds)}`);
        console.log(`Display CRS: ${data.display_crs}`);
        console.log(`Display dimensions: ${data.display_width} x ${data.display_height}`);
        console.log(`Display bounds: ${JSON.stringify(data.bounds)}`);
        
        const datasetMeta = {
            id: scene.scene_id,
            name: `Sentinel-2 (${scene.datetime.split('T')[0]})`,
            is_stac: true,
            bounds: data.bounds,
            preview_url: data.image_url,
            bands: [
                { id: 'True Color', description: 'Visual' },
                { id: 'B04', description: 'Red' },
                { id: 'B03', description: 'Green' },
                { id: 'B02', description: 'Blue' },
                { id: 'B08', description: 'NIR' }
            ],
            metadata: {
                crs: data.display_crs,
                width: data.display_width,
                height: data.display_height,
                dtype: 'uint8',
                driver: 'COG',
                resolution: 10,
                p2: 0,
                p98: 3000,
                source_crs: data.source_crs
            },
            scene_info: scene
        };
        
        const existingIndex = layers.findIndex(l => l.id === datasetMeta.id);
        if (existingIndex >= 0) {
            layers[existingIndex] = datasetMeta;
        } else {
            layers.push(datasetMeta);
        }
        clearLayerList();
        layers.forEach(addLayerToList);
        updateNoDataState();
        
        selectLayer(datasetMeta.id);
        document.getElementById('header-status').textContent = `STAC Scene loaded: ${datasetMeta.name}`;
        updateAnalysisSceneDropdown();
    } catch (e) {
        console.error(e);
        document.getElementById('header-status').textContent = `Error loading scene: ${e.message}`;
    }
}

function updateAnalysisSceneDropdown() {
    const sel = document.getElementById('analysis-scene');
    if (!sel) return;
    sel.innerHTML = '';
    const analysisSources = layers.filter(l => !l.is_analysis);
    if (analysisSources.length === 0) {
        sel.innerHTML = '<option value="">No dataset loaded...</option>';
        return;
    }
    analysisSources.forEach(l => {
        const opt = document.createElement('option');
        opt.value = l.id;
        
        let displayName = l.name;
        if (!l.is_stac) {
            const hasB04 = l.bands && l.bands.some(b => b.id === 'B04');
            const hasB08 = l.bands && l.bands.some(b => b.id === 'B08');
            const isMultiband = l.metadata && l.metadata.bands > 1;
            
            if (hasB04 && hasB08) {
                // If it already has B04 + B08 in the name, don't append it again
                if (!displayName.includes('B04')) {
                    displayName = displayName + " — B04 + B08";
                }
            } else if (isMultiband) {
                if (!displayName.includes('Multiband')) {
                    displayName = displayName + " (Multiband)";
                }
            } else if (hasB04 && !hasB08) {
                displayName = displayName + " — Missing B08";
            } else if (hasB08 && !hasB04) {
                displayName = displayName + " — Missing B04";
            }
        }
        
        opt.textContent = displayName;
        sel.appendChild(opt);
    });
}


const btnCalcNdvi = document.getElementById('btn-calc-ndvi');
if (btnCalcNdvi) {
    btnCalcNdvi.addEventListener('click', async () => {
        const layerId = document.getElementById('analysis-scene').value;
        if (!layerId) {
            alert("Load or upload a raster before calculating NDVI.");
            return;
        }
        
        const selectedLayer = layers.find(l => l.id === layerId);
        const source_type = selectedLayer.is_stac ? 'stac' : 'upload';
        
        btnCalcNdvi.disabled = true;
        btnCalcNdvi.textContent = 'Calculating...';
        document.getElementById('header-status').textContent = 'Calculating NDVI...';
        
        let aoiData = null;
        if (currentAOI) {
            aoiData = {
                type: 'bbox',
                shape: currentAOI.geometry_type,
                area: currentAOI.area_m2 || 0,
                north: currentAOI.bbox.north,
                south: currentAOI.bbox.south,
                east: currentAOI.bbox.east,
                west: currentAOI.bbox.west,
                geometry: currentAOI.geometry
            };
        }
        
        try {
            const res = await fetch('http://127.0.0.1:8000/api/v1/analysis/ndvi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scene_id: layerId, source_type: source_type, aoi: aoiData })
            });
            
            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || `HTTP Error ${res.status}`);
            }
            
            const data = await res.json();
            
            const parentLayer = layers.find(l => l.id === layerId);
            
            const datasetMeta = {
                id: `analysis:ndvi:${data.scene_id}`,
                name: `NDVI - ${data.scene_id.includes('_') ? data.scene_id.split('_')[2].split('T')[0] : data.scene_id.substring(0, 8)}`,
                  is_stac: false,
                is_analysis: true,
                  source_layer_name: parentLayer ? parentLayer.name : data.scene_id,
                  analysis_data: data,
                bounds: data.bounds,
                preview_url: data.image_url,
                bands: [{ id: 'NDVI', description: 'Vegetation Index' }],
                metadata: {
                    crs: 'EPSG:4326',
                    source_crs: parentLayer ? (parentLayer.metadata.source_crs || parentLayer.metadata.crs) : null,
                    resolution: parentLayer ? parentLayer.metadata.resolution : null,
                    dtype: 'float32',
                    driver: 'Analysis'
                },
                scene_info: parentLayer ? parentLayer.scene_info : null
            };
            
            const existingIndex = layers.findIndex(l => l.id === datasetMeta.id);
            if (existingIndex >= 0) {
                layers[existingIndex] = datasetMeta;
            } else {
                layers.push(datasetMeta);
            }
            clearLayerList();
            layers.forEach(addLayerToList);
            updateNoDataState();
            selectLayer(datasetMeta.id);
            document.getElementById('header-status').textContent = `NDVI calculated`;
            
        } catch (e) {
            console.error(e);
            alert(`NDVI calculation failed:\n${e.message}`);
            document.getElementById('header-status').textContent = 'NDVI failed';
        } finally {
            btnCalcNdvi.disabled = false;
            btnCalcNdvi.textContent = 'Calculate NDVI';
        }
    });
}
