const API_BASE = 'http://127.0.0.1:8000/api/v1/accidents';

const severityColors = {
  fatal: '#ff7777',
  severe: '#ffb45a',
  moderate: '#8dd8ff',
  minor: '#6bffa3'
};

const severityLabel = {
  fatal: 'Fatal',
  severe: 'Severe',
  moderate: 'Moderate',
  minor: 'Minor'
};

const severityClassMap = {
  fatal: 'status-critical',
  severe: 'status-high',
  moderate: 'status-medium',
  minor: 'status-low'
};

const accidentTypeLabel = {
  collision: 'Collision',
  pedestrian: 'Pedestrian',
  vehicle_rollover: 'Vehicle Rollover',
  head_on: 'Head On',
  rear_end: 'Rear End',
  side_impact: 'Side Impact',
  other: 'Other'
};

function init() {
  setClock();
  setTodayDate();
  bindEvents();
  loadDashboard();
}

document.addEventListener('DOMContentLoaded', init);

function bindEvents() {
  document.getElementById('stateFilter').addEventListener('change', (event) => {
    loadDashboard(event.target.value || '');
  });

  document.getElementById('incidentForm').addEventListener('submit', submitIncident);

  document.querySelectorAll('.view-button').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.view-button').forEach((b) => b.classList.toggle('active', b === button));
    });
  });
}

function setClock() {
  const now = new Date();
  const time = now.toISOString().slice(11, 19);
  document.getElementById('clockValue').textContent = time;
}

function setTodayDate() {
  const date = new Date();
  const formatted = date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
  document.getElementById('todayDate').textContent = formatted;
}

async function loadDashboard(state = '') {
  try {
    const stats = await fetchStats(state);
    updateStats(stats);
    await loadAccidents(state);
  } catch (error) {
    console.error(error);
    showFormMessage('Could not load data from the API service.', true);
  }
}

async function fetchJson(url, options = {}) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      let detail = 'Request failed';
      try {
        const payload = await response.json();
        detail = payload.detail || payload.message || detail;
      } catch (_) {
        detail = `HTTP ${response.status}`;
      }
      throw new Error(detail);
    }
    return await response.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}

async function fetchStats(state = '') {
  const params = new URLSearchParams();
  if (state) params.set('state', state);

  const url = `${API_BASE}/stats/summary?${params}`;
  return fetchJson(url);
}

async function loadAccidents(state = '') {
  const params = new URLSearchParams({ page: '1', page_size: '8' });
  if (state) params.set('state', state);

  const payload = await fetchJson(`${API_BASE}/?${params}`);
  const accidents = payload.accidents || [];

  const table = document.getElementById('accidentTable');
  if (!accidents.length) {
    table.innerHTML = `<tr><td colspan="8" class="table-empty">No accidents found</td></tr>`;
    return;
  }

  table.innerHTML = accidents.map(formatTableRow).join('');
}

function formatTableRow(accident) {
  const severity = accident.severity || 'minor';
  return `<tr>
      <td>#${accident.id}</td>
      <td>${escapeHtml(accident.location)}</td>
      <td>${escapeHtml(accident.state)}</td>
      <td>${escapeHtml(accident.district)}</td>
      <td>${accidentTypeLabel[accident.accident_type] || accident.accident_type}</td>
      <td><span class="status-badge ${severityClassMap[severity] || 'status-low'}">${severityLabel[severity] || severity}</span></td>
      <td>${accident.casualties || 0}</td>
      <td><span class="status-badge ${severityClassMap[severity] || 'status-low'}">${accident.verified ? 'Verified' : 'Open'}</span></td>
    </tr>`;
}

function updateStats(stats) {
  const total = stats.total_accidents || 0;
  const fatalities = stats.total_fatalities || 0;
  const injuries = stats.total_injuries || 0;
  const severityCounts = stats.severity_breakdown || {};

  document.getElementById('totalAccidents').textContent = total;
  document.getElementById('fatalityCount').textContent = fatalities;
  document.getElementById('injuryCount').textContent = injuries;

  const risk = clamp(
    Math.round(
      (severityCounts.fatal || 0) * 16 +
      (severityCounts.severe || 0) * 8 +
      (severityCounts.moderate || 0) * 4 +
      total * 0.5
    ),
    15,
    96
  );
  document.getElementById('riskIndex').textContent = `${risk}%`;
  document.getElementById('riskScore').textContent = `${risk}%`;

  const priority = getPriorityDistrict(stats.filters_applied?.state);
  document.getElementById('districtPriority').textContent = priority;

  const totalBreakdown = Math.max(Object.values(severityCounts).reduce((sum, n) => sum + n, 0), 1);
  const rows = [
    { key: 'fatal', selector: 'severity-critical', value: severityCounts.fatal || 0 },
    { key: 'severe', selector: 'severity-high', value: severityCounts.severe || 0 },
    { key: 'moderate', selector: 'severity-medium', value: severityCounts.moderate || 0 },
    { key: 'minor', selector: 'severity-low', value: severityCounts.minor || 0 }
  ];

  for (const row of rows) {
    const count = row.value || 0;
    const pct = clamp(Math.round((count / totalBreakdown) * 100), 0, 100);
    const percent = `${pct}%`;

    const rowHtml = document.querySelector(`.${row.selector}`);
    if (rowHtml) {
      rowHtml.style.width = percent;
    }

    const rowIndex = rows.findIndex(r => r.key === row.key);
    const valueCell = document.querySelector(`#severityBreakdown .severity-row:nth-child(${rowIndex + 1}) .severity-value`);
    if (valueCell) valueCell.textContent = count;
  }
}

async function submitIncident(event) {
  event.preventDefault();

  const location = document.getElementById('location').value.trim();
  const district = document.getElementById('district').value.trim();
  const state = document.getElementById('state').value;
  const accidentType = document.getElementById('accident_type').value;
  const severity = document.getElementById('severity').value;

  if (!location || !district || !state || !accidentType || !severity) {
    showFormMessage('Fill location, district, state, type, and severity before submitting.', true);
    return;
  }

  const payload = {
    location,
    latitude: Number(document.getElementById('latitude').value),
    longitude: Number(document.getElementById('longitude').value),
    state,
    district,
    accident_type: accidentType,
    severity,
    casualties: Number(document.getElementById('casualties').value),
    injuries: Number(document.getElementById('injuries').value),
    fatalities: Number(document.getElementById('fatalities').value),
    weather_condition: 'Clear',
    road_condition: 'Normal',
    time_of_day: 'Morning',
    description: document.getElementById('description').value,
    contributing_factors: 'Field report',
    reported_by: 'Field Operator',
  };

  try {
    const created = await fetchJson(API_BASE + '/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    showFormMessage(`Incident #${created.id} submitted successfully.`);
    event.target.reset();
    await loadDashboard();
  } catch (error) {
    console.error(error);
    showFormMessage(error.message || 'Unable to submit incident', true);
  }
}

function showFormMessage(message, isError = false) {
  const msg = document.getElementById('formMessage');
  msg.textContent = message;
  msg.style.color = isError ? 'var(--red)' : 'var(--green)';
}

function escapeHtml(value) {
  return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function getPriorityDistrict(state = '') {
  const defaultDistrict = 'Maharashtra / Pune';
  if (!state) return defaultDistrict;
  return `${state} / ${state === 'Delhi' ? 'South Delhi' : 'High Risk Corridor'}`;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}
