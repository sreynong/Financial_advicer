console.log("app.js loaded");
function safeChart(canvasId, config) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) {
    console.warn("Chart canvas not found:", canvasId);
    return;
  }
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    console.warn("Canvas context unavailable:", canvasId);
    return;
  }
  new Chart(ctx, config);
}

window.renderExpenseChart = function (categoryData) {
  if (!categoryData || !categoryData.length) return;
  safeChart("expenseChart", {
    type: "doughnut",
    data: {
      labels: categoryData.map((item) => item.category),
      datasets: [{ data: categoryData.map((item) => Number(item.total)) }],
    },
    options: { responsive: true, plugins: { legend: { position: "bottom" } } },
  });
};

wiconsole.log("renderTrendChart data:", trendData);
ndow.renderTrendChart = function (trendData) {
  console.log("renderTrendChart data:", trendData);
  if (!trendData || !trendData.length) {
    console.warn("Trend chart skipped: no trendData available.", trendData);
    return;
  }
  safeChart("trendChart", {
    type: "line",
    data: {
      labels: trendData.map((item) => item.label),
      datasets: [
        {
          label: "Income",
          data: trendData.map((item) => item.income),
          borderColor: "rgba(79, 70, 229, 0.9)",
          backgroundColor: "rgba(79, 70, 229, 0.25)",
          tension: 0.35,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: "Expense",
          data: trendData.map((item) => item.expense),
          borderColor: "rgba(239, 68, 68, 0.9)",
          backgroundColor: "rgba(239, 68, 68, 0.25)",
          tension: 0.35,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" },
        tooltip: { mode: "index", intersect: false },
      },
      scales: {
        x: { display: true },
        y: { display: true, beginAtZero: true },
      },
    },
  });
};

window.renderForecastChart = function (forecastData) {
  if (!forecastData || !forecastData.length) return;
  safeChart("forecastChart", {
    type: "bar",
    data: {
      labels: forecastData.map((item) => item.label),
      datasets: [
        {
          label: "Predicted Savings",
          data: forecastData.map((item) => item.predicted_savings),
        },
      ],
    },
    options: { responsive: true, plugins: { legend: { display: true } } },
  });
};

window.bindAIAdviceForm = function (endpoint) {
  const form = document.getElementById("aiAdviceForm");
  const resultBox = document.getElementById("aiAdviceResult");
  if (!form || !resultBox) return;

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    resultBox.textContent = "Loading advice...";
    const formData = new FormData(form);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      const data = await response.json();
      resultBox.textContent = data.success
        ? data.answer
        : data.error || "Something went wrong.";
    } catch (error) {
      resultBox.textContent = error.message || "Network error.";
    }
  });
};
