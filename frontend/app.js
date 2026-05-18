const API = "http://localhost:8000";

function switchTab(name) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(t => {
    t.classList.remove("active");
    t.classList.add("hidden");
  });
  event.target.classList.add("active");
  const section = document.getElementById(`tab-${name}`);
  section.classList.remove("hidden");
  section.classList.add("active");
}

// ─── MODULE 1 : CHECKER ────────────────────────────────────────────────────

async function runChecker() {
  const fileInput = document.getElementById("checker-file");
  const resultDiv = document.getElementById("checker-result");

  if (!fileInput.files.length) {
    alert("Sélectionne un fichier à analyser.");
    return;
  }

  resultDiv.innerHTML = loader("Analyse en cours...");
  resultDiv.classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch(`${API}/checker/upload`, { method: "POST", body: formData });
    if (!res.ok) {
      const err = await res.json();
      resultDiv.innerHTML = error(err.detail);
      return;
    }
    const data = await res.json();
    resultDiv.innerHTML = renderCheckerResult(data);
  } catch (e) {
    resultDiv.innerHTML = error("Impossible de contacter l'API. Le serveur est-il lancé ?");
  }
}

function renderCheckerResult(data) {
  const s = data.summary;
  const scoreColor = s.score >= 80 ? "ok" : s.score >= 50 ? "warning" : "danger";

  const cards = `
    <div class="summary-grid">
      <div class="summary-card"><div class="value ${scoreColor}">${s.score}%</div><div class="label">Score global</div></div>
      <div class="summary-card"><div class="value ok">${s.ok}</div><div class="label">Vérifiées</div></div>
      <div class="summary-card"><div class="value warning">${s.warning}</div><div class="label">Avertissements</div></div>
      <div class="summary-card"><div class="value danger">${s.not_found}</div><div class="label">Introuvables</div></div>
      <div class="summary-card"><div class="value danger">${s.suspect_semantic}</div><div class="label">Suspectes</div></div>
    </div>`;

  const refs = data.reports.map(r => {
    const semBadge = r.semantic
      ? `<span class="badge badge-${r.semantic.label}">${r.semantic.label} (${r.semantic.score})</span>`
      : "";
    const sentences = r.citing_sentences.length
      ? `<div class="ref-semantic">« ${r.citing_sentences[0].substring(0, 150)}… »</div>`
      : "";
    return `
      <div class="ref-card status-${r.verification.status}">
        <div class="ref-key">${escHtml(r.cite_key)}
          <span class="badge badge-${r.verification.status}">${r.verification.status}</span>
          ${semBadge}
          <span style="color:#718096;font-size:0.75rem;margin-left:8px">confiance: ${r.verification.confidence}</span>
        </div>
        <div class="ref-raw">${escHtml(r.raw_text)}</div>
        <div class="ref-message">${escHtml(r.verification.message)}</div>
        ${sentences}
      </div>`;
  }).join("");

  return `<h3 style="margin-bottom:16px">Rapport — ${data.total_references} référence(s) · format ${data.format}</h3>${cards}${refs}`;
}

// ─── MODULE 2 : RELATED WORK ───────────────────────────────────────────────

async function runRelatedWork() {
  const topic = document.getElementById("rw-topic").value.trim();
  const files = document.getElementById("rw-files").files;
  const doisRaw = document.getElementById("rw-dois").value.trim();
  const resultDiv = document.getElementById("rw-result");

  if (!files.length && !doisRaw) {
    alert("Upload des fichiers ou fournis une liste de DOIs.");
    return;
  }

  resultDiv.innerHTML = loader("Clustering et génération en cours (peut prendre 30–60 s)...");
  resultDiv.classList.remove("hidden");

  try {
    let data;

    if (doisRaw && !files.length) {
      const dois = doisRaw.split("\n").map(d => d.trim()).filter(Boolean);
      const res = await fetch(`${API}/related-work/generate-from-dois`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dois, topic: topic || "ce sujet de recherche" }),
      });
      if (!res.ok) { const e = await res.json(); resultDiv.innerHTML = error(e.detail); return; }
      data = await res.json();
    } else {
      const formData = new FormData();
      formData.append("topic", topic || "ce sujet de recherche");
      for (const f of files) formData.append("files", f);
      const res = await fetch(`${API}/related-work/generate`, { method: "POST", body: formData });
      if (!res.ok) { const e = await res.json(); resultDiv.innerHTML = error(e.detail); return; }
      data = await res.json();
    }

    resultDiv.innerHTML = renderRWResult(data);
  } catch (e) {
    resultDiv.innerHTML = error("Impossible de contacter l'API. Le serveur est-il lancé ?");
  }
}

function renderRWResult(data) {
  const clusterTags = data.clusters.map(c =>
    `<span class="rw-cluster-tag">${escHtml(c.label)} (${c.documents.length} docs)</span>`
  ).join("");

  const rwText = escHtml(data.related_work);

  return `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
      <h3>${data.document_count} documents · ${data.cluster_count} thèmes identifiés</h3>
      <button class="copy-btn" onclick="copyText()">Copier le texte</button>
    </div>
    <div class="rw-clusters">${clusterTags}</div>
    <div class="rw-text" id="rw-text-output">${rwText}</div>`;
}

function copyText() {
  const el = document.getElementById("rw-text-output");
  navigator.clipboard.writeText(el.innerText);
}

// ─── HELPERS ───────────────────────────────────────────────────────────────

function loader(msg) {
  return `<div class="loader"><div class="spinner"></div>${msg}</div>`;
}

function error(msg) {
  return `<div style="color:#fc8181;padding:16px">Erreur : ${escHtml(msg)}</div>`;
}

function escHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
