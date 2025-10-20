document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#tripTable tbody");
  const summaryContainer = document.querySelector("#summaryContainer");

  async function loadData() {
    try {
      const response = await fetch("http://127.0.0.1:5000/data");
      const data = await response.json();

      summaryContainer.innerHTML = `
        <p>Total Trips: ${data.length}</p>
        <p>Average Fare: $${(data.reduce((a, b) => a + b.fare_amount, 0) / data.length).toFixed(2)}</p>
        <p>Average Speed: ${(data.reduce((a, b) => a + b.speed, 0) / data.length).toFixed(2)} km/h</p>
      `;

      tableBody.innerHTML = data.map(row => `
        <tr>
          <td>${row.pickup_datetime}</td>
          <td>${row.dropoff_datetime}</td>
          <td>${row.distance_km.toFixed(2)}</td>
          <td>$${row.fare_amount.toFixed(2)}</td>
          <td>${row.speed.toFixed(2)}</td>
        </tr>
      `).join("");
    } catch (error) {
      summaryContainer.innerHTML = "⚠️ Error loading data from backend.";
      console.error(error);
    }
  }

  document.querySelector("#filterBtn").addEventListener("click", loadData);
  loadData();
});
