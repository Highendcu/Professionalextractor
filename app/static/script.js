// === Theme Toggle ===
function toggleTheme() {
  const body = document.body;
  const themeToggle = document.getElementById("theme-toggle");
  body.classList.toggle("light-mode");
  const isLight = body.classList.contains("light-mode");
  localStorage.setItem("theme", isLight ? "light" : "dark");
  themeToggle.innerText = isLight ? "🌙 Dark Mode" : "☀️ Light Mode";
}

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");
  const themeToggle = document.getElementById("theme-toggle");
  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
    if (themeToggle) themeToggle.innerText = "🌙 Dark Mode";
  }
  if (themeToggle) themeToggle.addEventListener("click", toggleTheme);

  // Modal Event Listener Bind
  document.querySelectorAll(".close-btn, #modal-overlay").forEach(el => {
    el.addEventListener("click", closeModals);
  });

  // Extraction Button
  const startBtn = document.getElementById("start-btn");
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      const urls = document.getElementById("urls").value.trim();
      const checkedPlatforms = document.querySelectorAll('input[name="platforms[]"]:checked');
      if (!urls || checkedPlatforms.length === 0) {
        alert("Please enter URLs and select at least one platform.");
        return;
      }
      openModal("login-modal");
    });
  }

  // Stop Extraction Button
  const stopBtn = document.getElementById("stop-btn");
  if (stopBtn) {
    stopBtn.addEventListener("click", () => {
      $.post("/stop-extraction", function () {
        clearInterval(extractionInterval);
        $('#loading-indicator').hide();
        showStatus("🛑 Extraction stopped", "warning");
      });
    });
  }

  // Export Button
  const exportBtn = document.querySelector(".success-btn[onclick*='exportData']");
  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      const entries = document.querySelectorAll(".data-entry td:first-child");
      const numbers = Array.from(entries).map(e => e.textContent.trim());
      if (numbers.length === 0) {
        alert("No numbers to export!");
        return;
      }
      const content = numbers.join("\n");
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "extracted_numbers.txt";
      a.click();
      URL.revokeObjectURL(url);
      showStatus("💾 Data exported!", "success");
    });
  }
});

// === Status Message Flash ===
function showStatus(message, type = "info") {
  const box = document.getElementById("status-box");
  if (!box) return;
  box.innerText = message;
  box.className = "status-box " + type;
  box.style.display = "block";
  setTimeout(() => {
    box.style.display = "none";
  }, 4000);
}

// === Print Extracted Data ===
function printExtractedData() {
  const preview = document.getElementById("phone-preview");
  if (!preview) return;
  const printContent = preview.parentElement.innerHTML;
  const printWindow = window.open("", "_blank");
  printWindow.document.write(`
    <html><head><title>Print Extracted Data</title>
    <link rel="stylesheet" href="/static/styles.css">
    </head><body>${printContent}</body></html>
  `);
  printWindow.document.close();
  printWindow.focus();
  printWindow.print();
  printWindow.close();
}

// === Modal Controls ===
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.add("active");
  const overlay = document.getElementById("modal-overlay");
  if (overlay) overlay.classList.add("active");
}

function closeModals() {
  document.querySelectorAll(".modal").forEach(modal => modal.classList.remove("active"));
  const overlay = document.getElementById("modal-overlay");
  if (overlay) overlay.classList.remove("active");
}

// === License Generator ===
function generateLicense(userId) {
  fetch("/generate-license", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ user_id: userId }),
  })
    .then(res => res.json())
    .then(data => {
      if (data.license_key) {
        alert("License Key: " + data.license_key);
      } else {
        alert("Error generating license.");
      }
    });
}

// === Extraction Logic ===
let extractionInterval;

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  $.post('/verify-credentials', { username, password }, function (data) {
    if (data.valid) {
      $('#login-modal').hide();
      $('#license-warning').hide();
      $('#loading-indicator').show();

      $.post('/extract', $('#phone-extractor-form').serialize(), function () {
        showStatus("✅ Extraction started!", "success");
      });
    } else {
      $('#license-warning').show();
      $('#error-message').show();
    }
  });
});

// === WebSocket Real-Time Updates ===
const socket = io();

socket.on("update", data => {
  document.getElementById("new-count").innerText = data.new_count;
  document.getElementById("total-count").innerText = data.total_count;
});

socket.on("extraction_update", data => {
  const container = document.getElementById("phone-preview");
  if (!container || !data.data) return;

  if (container.querySelector(".placeholder-msg")) {
    container.innerHTML = ""; // Clear placeholder
  }

  data.data.forEach(entry => {
    const row = document.createElement("tr");
    row.classList.add("data-entry");
    row.innerHTML = `
      <td>${entry.number || ""}</td>
      <td>${entry.name || ""}</td>
      <td>${entry.address || ""}</td>
    `;
    container.appendChild(row);
  });
});

// === Polling Fallback (optional) ===
function updateResults() {
  $.get("/view-extraction", function (data) {
    const container = document.getElementById("phone-preview");
    if (!container) return;
    container.innerHTML = "";
    data.numbers.forEach(entry => {
      container.innerHTML += `
        <tr class="data-entry">
          <td>${entry.number}</td>
          <td>${entry.name}</td>
          <td>${entry.address}</td>
        </tr>
      `;
    });
  });
}
