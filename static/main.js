const iot_data = [
  { date: "2025-05-30", time: "00:00 - 04:00", temperature: "25°C", humidity: "70%", co2: "60 ppm" },
  { date: "2025-05-30", time: "04:00 - 08:00", temperature: "26°C", humidity: "68%", co2: "62 ppm" },
  { date: "2025-05-30", time: "08:00 - 12:00", temperature: "27°C", humidity: "65%", co2: "58 ppm" }
];

// Initialize index
let dataIndex = 0;

function updateData() {
  const data = iot_data[dataIndex];
  document.getElementById("date").innerText = data.date;
  document.getElementById("time").innerText = data.time;
  document.getElementById("temperature").innerText = data.temperature;
  document.getElementById("humidity").innerText = data.humidity;
  document.getElementById("co2").innerText = data.co2;

  dataIndex = (dataIndex + 1) % iot_data.length;
}


document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      const $table = $("table.iot-table");
      if ($table.length) {
        $table.addClass("table table-bordered table-hover table-striped");
        $table.DataTable({
          pageLength: 5,
          lengthMenu: [5, 10, 25, 50, 100],
          language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records..."
          }
        });
      }
    }, 10); 
  });

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
      const $table = $("predictions");
      if ($table.length) {
        $table.addClass("table table-bordered table-hover table-striped");
        $table.DataTable({
          pageLength: 5,
          lengthMenu: [5, 10, 25, 50, 100],
          language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records..."
          }
        });
      }
    }, 10); 
  });

const themeToggleBtn = document.getElementById('theme-toggle');
  
  function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);
    themeToggleBtn.textContent = theme === 'dark' ? '☀️' : '🌙'; // sun for dark mode on (to switch to light), moon for light mode
    const nav = document.getElementById('navigation'); // Make sure your <nav> has id="navigation"
    nav.style.backgroundColor = '#212529'; // Light blue for light mode

  }

  // Load saved theme or default to dark
  const savedTheme = localStorage.getItem('theme') || 'dark';
  setTheme(savedTheme);

  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  });
  