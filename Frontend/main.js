const processBtn = document.getElementById('processBtn');
const vendorFilter = document.getElementById('vendorFilter');

// Summary elements
const totalTripsEl = document.getElementById('totalTrips');
const avgDistanceEl = document.getElementById('avgDistance');
const avgSpeedEl = document.getElementById('avgSpeed');
const avgFareEl = document.getElementById('avgFare');

// Charts
let tripsChart, fareChart;

// Initialize map
const map = L.map('map').setView([40.7128, -74.0060], 12); // NYC center
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let heatLayer;

processBtn.addEventListener('click', async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/process-data');
    const data = await response.json();

    // Update summary
    totalTripsEl.textContent = data.summary.total_trips;
    avgDistanceEl.textContent = data.summary.avg_distance_km.toFixed(2);
    avgSpeedEl.textContent = data.summary.avg_speed_kmh.toFixed(2);
    avgFareEl.textContent = data.summary.avg_fare ? data.summary.avg_fare.toFixed(2) : 'N/A';

    // Mock data for charts (replace with API data if available)
    const vendors = ['GoTaxi', 'Move'];
    const tripsPerVendor = [Math.floor(data.summary.total_trips * 0.6), Math.floor(data.summary.total_trips * 0.4)];
    const avgFarePerVendor = [5, 7];

    // Trips chart
    if (tripsChart) tripsChart.destroy();
    const ctx1 = document.getElementById('tripsChart').getContext('2d');
    tripsChart = new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: vendors,
        datasets: [{
          label: 'Total Trips',
          data: tripsPerVendor,
          backgroundColor: ['#3498db','#e74c3c']
        }]
      },
      options: { responsive: true }
    });

    // Fare chart
    if (fareChart) fareChart.destroy();
    const ctx2 = document.getElementById('fareChart').getContext('2d');
    fareChart = new Chart(ctx2, {
      type: 'line',
      data: {
        labels: vendors,
        datasets: [{
          label: 'Average Fare ($)',
          data: avgFarePerVendor,
          borderColor: '#2ecc71',
          fill: false,
          tension: 0.3
        }]
      },
      options: { responsive: true }
    });

    // Heatmap: replace with real trip coordinates
    const heatPoints = [
      [40.7128, -74.0060, 0.5],
      [40.730610, -73.935242, 0.7],
      [40.758896, -73.985130, 0.9]
    ];

    if (heatLayer) map.removeLayer(heatLayer);
    heatLayer = L.heatLayer(heatPoints, {radius: 25, blur: 15, maxZoom: 17}).addTo(map);

  } catch (err) {
    console.error('Error fetching data:', err);
    alert('Failed to fetch data from the backend.');
  }
});
