const API_BASE = "http://127.0.0.1:5000/api";
const form = document.querySelector("#predict-form");
const button = document.querySelector("#predict-button");
const message = document.querySelector("#form-message");

const controls = [
  ["study_hours", "study-value", v => Number(v).toFixed(1)],
  ["attendance", "attendance-value", v => String(v)],
  ["previous_marks", "previous-value", v => String(v)],
  ["assignment_score", "assignment-value", v => String(v)]
];

controls.forEach(([id, outputId, format]) => {
  const input = document.getElementById(id);
  const output = document.getElementById(outputId);
  const update = () => {
    output.textContent = format(input.value);
    const pct = (Number(input.value) - Number(input.min)) / (Number(input.max) - Number(input.min)) * 100;
    input.style.background = `linear-gradient(90deg, var(--mint) ${pct}%, #34435b ${pct}%)`;
  };
  input.addEventListener("input", update);
  update();
});

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `API request failed (${response.status})`);
  return data;
}

function showMessage(text, error = false) {
  message.textContent = text;
  message.classList.toggle("error", error);
}

async function checkHealth() {
  const dot = document.querySelector("#api-dot");
  const status = document.querySelector("#api-status");
  try {
    const data = await api("/health");
    dot.className = "online";
    status.textContent = data.model_loaded ? "API connected · model ready" : "API connected · model missing";
  } catch {
    dot.className = "offline";
    status.textContent = "API offline";
  }
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  button.disabled = true;
  button.textContent = "Predicting…";
  showMessage("");
  const payload = Object.fromEntries(controls.map(([id]) => [id, Number(document.getElementById(id).value)]));
  try {
    const result = await api("/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    document.querySelector("#score-value").textContent = Number(result.predicted_marks).toFixed(1);
    document.querySelector("#score-fill").style.width = `${result.predicted_marks}%`;
    document.querySelector("#score-description").textContent =
      result.predicted_marks < 40 ? "This estimate is low. A consistent study plan and teacher support may help." :
      result.predicted_marks < 70 ? "This estimate is in the middle range. Regular practice may help." :
      "This estimate is relatively high. Keep practising and revising.";
    document.querySelector("#result-time").textContent =
      new Date(result.created_at).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
    showMessage("Prediction complete. This is an estimate based on synthetic demo data.");
    await loadHistory();
  } catch (err) {
    showMessage(`${err.message} Check that the backend is running and the model is trained.`, true);
  } finally {
    button.disabled = false;
    button.innerHTML = '✦ &nbsp; Predict exam marks <span>↗</span>';
    checkHealth();
  }
});

async function loadStats() {
  try {
    const data = await api("/stats");
    document.querySelector("#dataset-rows").textContent = data.dataset_rows ?? "—";
    if (data.metrics) {
      document.querySelector("#mae-value").textContent = Number(data.metrics.mae).toFixed(2);
      document.querySelector("#r2-value").textContent = Number(data.metrics.r2).toFixed(2);
      document.querySelector("#metrics-note").textContent =
        `Test set: ${data.metrics.test_rows} records. Synthetic data only; not real-world validation.`;
    } else {
      document.querySelector("#metrics-note").textContent = "Train the model to load evaluation metrics.";
    }
  } catch {
    document.querySelector("#metrics-note").textContent = "Backend unavailable. Start the Flask server and refresh.";
  }
}

async function loadHistory() {
  const body = document.querySelector("#history-body");
  try {
    const data = await api("/history");
    if (!data.history.length) {
      body.innerHTML = '<tr><td colspan="6" class="empty">No predictions yet. Make your first prediction above.</td></tr>';
      return;
    }
    body.innerHTML = data.history.map(row => {
      const time = new Date(row.created_at).toLocaleString([], {month:"short", day:"numeric", hour:"2-digit", minute:"2-digit"});
      return `<tr><td>${time}</td><td>${Number(row.study_hours).toFixed(1)} hrs</td><td>${Number(row.attendance).toFixed(0)}%</td><td>${Number(row.previous_marks).toFixed(1)}</td><td>${Number(row.assignment_score).toFixed(1)}</td><td>${Number(row.predicted_marks).toFixed(1)} / 100</td></tr>`;
    }).join("");
  } catch {
    body.innerHTML = '<tr><td colspan="6" class="empty">Could not load history. Check backend connection.</td></tr>';
  }
}

document.querySelector("#refresh-history").addEventListener("click", loadHistory);
checkHealth();
loadStats();
loadHistory();
