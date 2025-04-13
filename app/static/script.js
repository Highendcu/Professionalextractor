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
  if (savedTheme === "light") {
    document.body.classList.add("light-mode");
    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) themeToggle.innerText = "🌙 Dark Mode";
  }

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) themeToggle.addEventListener("click", toggleTheme);
});

// === Status Message Flash ===
function showStatus(message, type = "info") {
  const box = document.getElementById("status-box");
  if (!box) return;
  box.innerText = message;
  box.className = "status-box " + type;
  box.style.display = "block";
  setTimeout(() => { box.style.display = "none"; }, 4000);
}

// === Print Functionality ===
function printExtractedData() {
  const printContent = document.getElementById("phone-preview").parentElement.innerHTML;
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
  document.getElementById(id).classList.add("active");
  document.getElementById("modal-overlay").classList.add("active");
}

function closeModals() {
  document.querySelectorAll(".modal").forEach(modal => modal.classList.remove("active"));
  document.getElementById("modal-overlay").classList.remove("active");
}

document.querySelectorAll(".close-btn, #modal-overlay").forEach(el => {
  el.addEventListener("click", closeModals);
});

// === Extraction Logic ===
let extractionInterval;

document.getElementById("start-btn").addEventListener("click", () => {
  const urls = document.getElementById("urls").value.trim();
  const checkedPlatforms = document.querySelectorAll('input[name="platforms[]"]:checked');

  if (!urls || checkedPlatforms.length === 0) {
    alert("Please enter URLs and select at least one platform.");
    return;
  }

  openModal("login-modal");
});

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  $.post('/verify-credentials', { username, password }, function (data) {
    if (data.valid) {
      $('#login-modal').hide();
      $('#license-warning').hide();
      $('#loading-indicator').show(); // 👈 show loader + text
      $.post('/extract', $('#phone-extractor-form').serialize(), function () {
        extractionInterval = setInterval(updateResults, 5000);
        showStatus("✅ Extraction started!", "success");
      });
    } else {
      $('#license-warning').show();
      $('#error-message').show();
    }
  });
});

// === Live Updates ===
function updateResults() {
  $.get("/view-extraction", function (data) {
    const container = document.getElementById("phone-preview");
    container.innerHTML = "";
    data.numbers.forEach(entry => {
      container.innerHTML += `
        <tr class="data-entry">
          <td> ${entry.number}</td>
          <td> ${entry.name}</td>
          <td> ${entry.address}</td>
        </tr>
      `;
    });
  });
}

const socket = io();
socket.on("update", data => {
  document.getElementById("new-count").innerText = data.new_count;
  document.getElementById("total-count").innerText = data.total_count;
  updateResults();
});

// === Stop Extraction ===
document.getElementById("stop-btn").addEventListener("click", () => {
  $.post("/stop-extraction", function () {
    clearInterval(extractionInterval);
    $('#loading-indicator').hide(); // 👈 hide loader
    showStatus("🛑 Extraction stopped", "warning");
  });
});

// === Export Button ===
document.querySelector(".success-btn[onclick*='exportData']").addEventListener("click", () => {
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
