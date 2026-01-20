const lat = parseFloat(localStorage.getItem("lat")) || 27.0301;
const lon = parseFloat(localStorage.getItem("lon")) || 75.8947;

const map = L.map('map').setView([lat, lon], 17);
// 📍 User location marker (blue dot)
const userLocation = L.circleMarker([lat, lon], {
  radius: 8,
  fillColor: "#1E90FF",
  color: "#ffffff",
  weight: 2,
  opacity: 1,
  fillOpacity: 0.9
}).addTo(map);
// 🎯 Accuracy circle (simulated GPS accuracy ~50m)
const accuracyCircle = L.circle([lat, lon], {
  radius: 50, // meters
  color: "#1E90FF",
  fillColor: "#1E90FF",
  fillOpacity: 0.15,
  weight: 1
}).addTo(map);
// 🔍 Solar analysis radius (1 km)
const analysisRadius = L.circle([lat, lon], {
  radius: 1000, // 1 km
  color: "orange",
  fillColor: "orange",
  fillOpacity: 0.05,
  weight: 2,
  dashArray: "6,6"
}).addTo(map);

analysisRadius.bindPopup("🔍 Solar analysis radius (1 km)");



userLocation.bindPopup("📍 Selected Location");


console.log("map.js loaded");



L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);
// 🧭 Legend
const legend = L.control({ position: "bottomright" });

legend.onAdd = function () {
  const div = L.DomUtil.create("div", "legend");
  div.innerHTML = `
    <div style="background:white; padding:10px; border-radius:6px;
                box-shadow:0 0 10px rgba(0,0,0,0.2); font-size:14px;">
      <b>Legend</b><br>
      <span style="color:#1E90FF;">●</span> Selected Location<br>
      <span style="color:green;">■</span> Excellent Roof<br>
      <span style="color:yellow;">■</span> Good Roof<br>
      <span style="color:red;">■</span> Poor Roof<br>
      <span style="color:orange;">—</span> Analysis Radius
    </div>
  `;
  return div;
};

legend.addTo(map);
// 🔄 Reset location button
document.getElementById("resetBtn").onclick = () => {
  localStorage.removeItem("lat");
  localStorage.removeItem("lon");
  window.location.href = "index.html";
};


