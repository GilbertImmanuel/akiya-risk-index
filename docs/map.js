const L = window.L;
const DATA_BASE = new URL("data/", document.baseURI);
const JAPAN_BOUNDS = [[30.5, 129.0], [45.5, 145.5]];

const state = {
  meta: null,
  panel: [],
  panelByCode: new Map(),
  map: null,
  layer: null,
  mapReady: false,
  metric: "dilapidated",
  mapSize: { width: 0, height: 0 },
};

const els = {
  map: document.getElementById("map"),
  status: document.getElementById("map-status"),
  tooltip: document.getElementById("map-tooltip"),
  reset: document.getElementById("map-reset"),
  select: document.getElementById("metric-select"),
  definition: document.getElementById("metric-definition"),
  note: document.getElementById("metric-note"),
  legend: document.getElementById("legend"),
  summary: document.getElementById("summary"),
  top: document.getElementById("top-list"),
  bottom: document.getElementById("bottom-list"),
};

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function setStatus(message, isError = false) {
  if (!els.status) return;
  els.status.replaceChildren();
  if (!message) {
    els.status.hidden = true;
    return;
  }
  const text = document.createElement("p");
  text.textContent = message;
  els.status.append(text);
  if (isError) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "map-reload";
    button.textContent = "Reload data";
    button.addEventListener("click", () => window.location.reload());
    els.status.append(button);
  }
  els.status.hidden = false;
}

async function loadJson(name) {
  const response = await fetch(new URL(name, DATA_BASE));
  if (!response.ok) throw new Error(`${name}: ${response.status}`);
  return response.json();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function number(value, digits) {
  return Number(value).toLocaleString("en-US", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function formatValue(metric, recordOrValue) {
  const isRecord = typeof recordOrValue === "object" && recordOrValue !== null;
  const value = isRecord ? recordOrValue[metric.key] : recordOrValue;
  if (value === null || value === undefined || Number.isNaN(value)) return "No data";
  if (metric.format === "percent") return `${number(value, 1)}%`;
  if (metric.format === "pp") return `${value > 0 ? "+" : ""}${number(value, 1)} pp`;
  if (metric.format === "index") return number(value, 2);
  if (metric.format === "density") {
    if (value === 0) return "No station";
    const suffix = isRecord && recordOrValue.station_count > 0
      ? ` (${number(recordOrValue.station_count, 0)} stations)`
      : "";
    return `${number(value, 1)} per 100 km²${suffix}`;
  }
  return number(value, 1);
}

function styleForFeature(feature) {
  const metric = state.meta.metrics[state.metric];
  const cls = feature.properties[`class_${state.metric}`];
  const fill = cls === 0 || cls == null ? metric.no_data : metric.colors[cls - 1];
  return {
    color: "rgba(255,255,255,0.88)",
    weight: 0.7,
    opacity: 1,
    fillColor: fill,
    fillOpacity: 0.82,
  };
}

function popupHtml(record) {
  const metrics = state.meta.metrics;
  const rows = Object.entries(metrics)
    .map(([key, metric]) => {
      return `<dt>${escapeHtml(metric.short_label)}</dt><dd>${escapeHtml(formatValue(metric, record))}</dd>`;
    })
    .join("");
  return `
    <div class="popup">
      <p class="popup-kicker">${escapeHtml(record.prefecture)}</p>
      <h3>${escapeHtml(record.name)}</h3>
      <p class="popup-level">${escapeHtml(record.level)}</p>
      <dl>${rows}</dl>
      <p class="popup-source">Housing and Land Survey 2023; Census 2020 and 2025; FY2022 fiscal; KSJ N02 and S12.</p>
    </div>
  `;
}

function showTooltip(event, record) {
  if (!els.tooltip) return;
  const metric = state.meta.metrics[state.metric];
  els.tooltip.replaceChildren();
  const name = document.createElement("strong");
  name.textContent = record.name;
  const where = document.createElement("span");
  where.className = "tooltip-where";
  where.textContent = record.prefecture;
  const value = document.createElement("span");
  value.className = "tooltip-value";
  value.textContent = `${metric.short_label}: ${formatValue(metric, record)}`;
  els.tooltip.append(name, where, value);
  els.tooltip.hidden = false;
  moveTooltip(event);
}

function moveTooltip(event) {
  if (!els.tooltip || els.tooltip.hidden) return;
  const point = event.containerPoint || event.originalEvent;
  const width = 240;
  const left = Math.min(point.x + 14, state.mapSize.width - width - 8);
  const top = Math.min(point.y + 14, state.mapSize.height - 90);
  els.tooltip.style.left = `${Math.max(8, left)}px`;
  els.tooltip.style.top = `${Math.max(8, top)}px`;
}

function hideTooltip() {
  if (els.tooltip) els.tooltip.hidden = true;
}

function bindFeature(feature, layer) {
  const record = state.panelByCode.get(feature.properties.code);
  if (!record) return;

  layer.bindPopup(popupHtml(record), {
    maxWidth: 340,
    className: "akiya-popup",
    closeButton: true,
  });

  layer.on("mouseover", (event) => {
    layer.setStyle({ weight: 2, color: "#17232D" });
    layer.bringToFront();
    showTooltip(event, record);
  });
  layer.on("mousemove", moveTooltip);
  layer.on("mouseout", () => {
    layer.setStyle(styleForFeature(feature));
    hideTooltip();
  });
  layer.on("click", (event) => {
    layer.openPopup(event.latlng);
  });
}

function initMap(geojson) {
  const map = L.map("map", {
    zoomControl: false,
    attributionControl: true,
    minZoom: 3,
    maxZoom: 9,
  }).fitBounds(JAPAN_BOUNDS, { padding: [18, 18] });

  L.control.zoom({ position: "topright" }).addTo(map);
  L.tileLayer("https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png", {
    attribution: "国土地理院",
    maxZoom: 9,
    opacity: 0.8,
  }).addTo(map);

  const layer = L.geoJSON(geojson, {
    style: styleForFeature,
    onEachFeature: bindFeature,
  }).addTo(map);

  state.map = map;
  state.layer = layer;
  state.mapSize = { width: els.map.clientWidth, height: els.map.clientHeight };
  map.on("resize", () => {
    state.mapSize = { width: els.map.clientWidth, height: els.map.clientHeight };
  });
  state.mapReady = true;
  setMetric(state.metric);
  setStatus(null);
  window.akiyaMapReady = true;
}

function legendRow(color, label) {
  const row = document.createElement("div");
  row.className = "legend-row";
  const swatch = document.createElement("span");
  swatch.className = "legend-swatch";
  swatch.style.backgroundColor = color;
  const text = document.createElement("span");
  text.textContent = label;
  row.append(swatch, text);
  return row;
}

function renderLegend(key, metric) {
  els.legend.replaceChildren();
  metric.labels.forEach((label, index) => {
    els.legend.append(legendRow(metric.colors[index], label));
  });
  const hasNoData = state.panel.some((record) => record[key] == null);
  if (hasNoData) els.legend.append(legendRow(metric.no_data, "No data"));
}

function median(values) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function percentile(values, p) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor((sorted.length - 1) * p)];
}

function summaryRow(label, value) {
  const row = document.createElement("div");
  const term = document.createElement("dt");
  term.textContent = label;
  const detail = document.createElement("dd");
  detail.textContent = value;
  row.append(term, detail);
  return row;
}

function renderSummary(key, metric) {
  const values = state.panel.map((record) => record[key]).filter((value) => value != null);
  const missing = state.panel.length - values.length;
  els.summary.replaceChildren();
  els.summary.append(summaryRow("Median", formatValue(metric, median(values))));
  els.summary.append(summaryRow("90th percentile", formatValue(metric, percentile(values, 0.9))));
  els.summary.append(summaryRow("With data", number(values.length, 0)));
  if (missing > 0) els.summary.append(summaryRow("No data", number(missing, 0)));
}

function rankRow(record, metric) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "rank-row";

  const label = document.createElement("span");
  label.className = "rank-label";
  const name = document.createElement("span");
  name.className = "rank-name";
  name.textContent = record.name;
  const pref = document.createElement("span");
  pref.className = "rank-pref";
  pref.textContent = record.prefecture;
  label.append(name, pref);

  const value = document.createElement("span");
  value.className = "rank-value";
  value.textContent = formatValue(metric, record);

  button.append(label, value);
  button.addEventListener("click", () => flyToCode(record.code));
  return button;
}

function renderRanks(key, metric) {
  const rows = state.panel.filter((record) => record[key] != null);
  const high = [...rows].sort((a, b) => b[key] - a[key]).slice(0, 5);
  const low = [...rows].sort((a, b) => a[key] - b[key]).slice(0, 5);
  els.top.replaceChildren(...high.map((record) => rankRow(record, metric)));
  els.bottom.replaceChildren(...low.map((record) => rankRow(record, metric)));
}

function renderPanel(key, metric) {
  els.definition.textContent = metric.definition;
  els.note.textContent = metric.note || "";
  els.note.hidden = !metric.note;
  renderLegend(key, metric);
  renderSummary(key, metric);
  renderRanks(key, metric);
}

function setMetric(key) {
  const metric = state.meta?.metrics?.[key];
  if (!metric) return;
  state.metric = key;
  const url = new URL(window.location.href);
  if (url.searchParams.get("metric") !== key) {
    url.searchParams.set("metric", key);
    window.history.replaceState(null, "", url.toString());
  }
  if (els.select && els.select.value !== key) els.select.value = key;
  renderPanel(key, metric);
  hideTooltip();
  if (state.layer) state.layer.setStyle(styleForFeature);
}

function flyToCode(code) {
  if (!state.mapReady) return;
  const record = state.panelByCode.get(code);
  if (!record || record.lat == null || record.lon == null) return;
  const duration = reducedMotion() ? 0 : 0.6;
  state.map.flyTo([record.lat, record.lon], 7, { duration });
  L.popup({ maxWidth: 340, className: "akiya-popup", closeButton: true })
    .setLatLng([record.lat, record.lon])
    .setContent(popupHtml(record))
    .openOn(state.map);
}

function resetView() {
  if (!state.mapReady) return;
  state.map.flyToBounds(JAPAN_BOUNDS, {
    padding: [18, 18],
    duration: reducedMotion() ? 0 : 0.6,
  });
}

async function init() {
  setStatus("Loading map data…");
  try {
    const [meta, panel, geojson] = await Promise.all([
      loadJson("meta.json"),
      loadJson("panel.json"),
      loadJson("municipalities.geojson"),
    ]);
    if (!Array.isArray(panel) || panel.length !== meta.unit_count) {
      throw new Error("Panel record count does not match metadata");
    }
    if (!geojson.features || geojson.features.length !== meta.unit_count) {
      throw new Error("Feature count does not match metadata");
    }
    state.meta = meta;
    state.panel = panel;
    state.panelByCode = new Map(panel.map((record) => [record.code, record]));
    const requested = new URLSearchParams(window.location.search).get("metric");
    if (requested && meta.metrics[requested]) state.metric = requested;
    if (els.select) els.select.value = state.metric;
    initMap(geojson);
    setMetric(state.metric);
  } catch (error) {
    console.error(error);
    setStatus("The map data could not be loaded. Check the network and reload.", true);
  }
}

if (els.reset) els.reset.addEventListener("click", resetView);
if (els.select) {
  els.select.addEventListener("change", (event) => setMetric(event.target.value));
}

window.addEventListener("akiya-metric", (event) => {
  const key = event.detail?.metric;
  if (typeof key === "string") setMetric(key);
});

window.akiyaAtlas = {
  setMetric,
  flyToCode,
  resetView,
  get metric() {
    return state.metric;
  },
  get ready() {
    return state.mapReady;
  },
  get map() {
    return state.map;
  },
  get layer() {
    return state.layer;
  },
};

init();
