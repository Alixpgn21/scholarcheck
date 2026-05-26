const API = "http://localhost:8000";

function switchTab(name, btnEl) {
  document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach(t => {
    t.classList.remove("active");
    t.classList.add("hidden");
  });
  const btn = btnEl || document.querySelector(`.tab-btn[data-tab="${name}"]`);
  btn.classList.add("active");
  const section = document.getElementById(`tab-${name}`);
  section.classList.remove("hidden");
  section.classList.add("active");
  moveIndicator(btn);
}

function moveIndicator(activeBtn) {
  const indicator = document.getElementById("tab-indicator");
  if (!indicator || !activeBtn) return;
  // offsetLeft is relative to offsetParent (.tab-nav has position:relative)
  indicator.style.left  = activeBtn.offsetLeft + "px";
  indicator.style.width = activeBtn.offsetWidth + "px";
}

document.addEventListener("DOMContentLoaded", () => {
  // Init indicator position on first active tab
  const activeBtn = document.querySelector(".tab-btn.active");
  if (activeBtn) {
    // Small delay so layout is settled
    requestAnimationFrame(() => moveIndicator(activeBtn));
  }

  document.getElementById("checker-file").addEventListener("change", (e) => {
    const file = e.target.files[0];
    const label = document.querySelector(".upload-text");
    if (file) {
      label.textContent = `Fichier prêt : ${file.name}`;
      label.style.color = "var(--green)";
    } else {
      label.textContent = "Glisse ton manuscrit ici ou clique";
      label.style.color = "";
    }
  });

  document.getElementById("rw-files").addEventListener("change", (e) => {
    const files = e.target.files;
    const label = document.getElementById("rw-files-label");
    if (files.length > 0) {
      label.textContent = `${files.length} fichier(s) sélectionné(s)`;
      label.style.color = "var(--green)";
    } else {
      label.textContent = "Choisir des fichiers .tex / .docx / .md";
      label.style.color = "";
    }
  });

  checkApiStatus();
});

async function checkApiStatus() {
  const dot = document.querySelector(".api-dot");
  try {
    const res = await fetch(`${API}/health`, { signal: AbortSignal.timeout(3000) });
    if (res.ok) {
      dot.classList.remove("offline");
    } else {
      dot.classList.add("offline");
    }
  } catch {
    dot.classList.add("offline");
  }
}

// ─── MODULE 1 : CHECKER ────────────────────────────────────────────────────

async function runChecker() {
  const fileInput = document.getElementById("checker-file");
  const resultDiv = document.getElementById("checker-result");

  if (!fileInput.files.length) {
    alert("Selectionne un fichier a analyser.");
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
    resultDiv.innerHTML = error("Impossible de contacter l'API. Le serveur est-il lance ?");
  }
}

function renderCheckerResult(data) {
  const s = data.summary;
  const scoreColor = s.score >= 80 ? "ok" : s.score >= 50 ? "warning" : "danger";

  const metrics = `
    <div class="metrics-row">
      <div class="metric"><div class="number ${scoreColor}">${s.score}%</div><div class="desc">Score</div></div>
      <div class="metric"><div class="number ok">${s.ok}</div><div class="desc">Verifiees</div></div>
      <div class="metric"><div class="number warning">${s.warning}</div><div class="desc">Alertes</div></div>
      <div class="metric"><div class="number danger">${s.not_found}</div><div class="desc">Introuvables</div></div>
      <div class="metric"><div class="number danger">${s.suspect_semantic}</div><div class="desc">Suspectes</div></div>
    </div>`;

  const refs = data.reports.map(r => {
    const semBadge = r.semantic
      ? `<span class="badge badge-${r.semantic.label}">${r.semantic.label} (${r.semantic.score})</span>`
      : "";
    const sentences = r.citing_sentences.length
      ? `<div class="ref-semantic">&laquo; ${escHtml(r.citing_sentences[0].substring(0, 150))}&hellip; &raquo;</div>`
      : "";
    return `
      <div class="ref-card status-${r.verification.status}">
        <div class="ref-header">
          <span class="ref-key">${escHtml(r.cite_key)}</span>
          <span class="badge badge-${r.verification.status}">${r.verification.status}</span>
          ${semBadge}
          <span class="ref-confidence">${r.verification.confidence}</span>
        </div>
        <div class="ref-raw">${escHtml(r.raw_text)}</div>
        <div class="ref-message">${escHtml(r.verification.message)}</div>
        ${sentences}
      </div>`;
  }).join("");

  return `
    <div class="report-title">
      Rapport
      <span class="tag">${data.total_references} ref.</span>
      <span class="tag">${data.format}</span>
    </div>
    ${metrics}
    <div class="ref-list">${refs}</div>`;
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

  resultDiv.innerHTML = loader("Clustering et generation en cours (30-60 s)...");
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
    resultDiv.innerHTML = error("Impossible de contacter l'API. Le serveur est-il lance ?");
  }
}

function renderRWResult(data) {
  const clusterTags = (data.clusters || []).map(c =>
    `<span class="rw-cluster-tag">${escHtml(c.label)} (${c.documents.length})</span>`
  ).join("");

  const rwText = escHtml(data.related_work);

  return `
    <div class="rw-header">
      <h3>${data.document_count} documents &middot; ${data.cluster_count} themes</h3>
      <button class="copy-btn" onclick="copyText()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
        </svg>
        Copier
      </button>
    </div>
    <div class="rw-clusters">${clusterTags}</div>
    <div class="rw-text" id="rw-text-output">${rwText}</div>`;
}

function copyText() {
  const el = document.getElementById("rw-text-output");
  navigator.clipboard.writeText(el.innerText);
  const btn = document.querySelector(".copy-btn");
  const original = btn.innerHTML;
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Copie !`;
  btn.style.color = "var(--green)";
  btn.style.borderColor = "var(--green)";
  setTimeout(() => {
    btn.innerHTML = original;
    btn.style.color = "";
    btn.style.borderColor = "";
  }, 1500);
}

// ─── HELPERS ───────────────────────────────────────────────────────────────

function loader(msg) {
  return `<div class="loader"><div class="spinner"></div>${msg}</div>`;
}

function error(msg) {
  return `<div class="error-msg">Erreur : ${escHtml(msg)}</div>`;
}

function escHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
