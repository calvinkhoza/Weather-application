 // Function to fetch weather data from the Flask API
 async function fetchWeatherData() {
    try {
      const response = await fetch('http://localhost:5000/weather');
      const data = await response.json();
      updateWeatherUI(data);
    } catch (error) {
      console.error('Error fetching weather data:', error);
    }
  }

  // Function to update the UI with the fetched weather data
  function updateWeatherUI(weatherData) {
    const forecastContainer = document.getElementById('forecast-container');
    const subtitle = document.getElementById('subtitle');
    const forecastCards = document.getElementById('forecast-cards');

    // Clear previous content
    forecastContainer.innerHTML = '';
    subtitle.innerHTML = '';
    forecastCards.innerHTML = '';

    if (Object.keys(weatherData).length === 0) {
      forecastContainer.innerHTML = '<p>No weather data available.</p>';
      return;
    }

    // Example: Update the UI with the weather data
    const cityName = weatherData.city || 'Unknown City';
    const temperatureF = weatherData.temperature || 'N/A';
    const description = weatherData.description || 'N/A';

    // Convert Fahrenheit to Celsius
    const temperatureC = temperatureF !== 'N/A' ? ((temperatureF - 32) * (5 / 9)).toFixed(2) : 'N/A';

    forecastContainer.innerHTML = `<h2>${cityName}</h2>`;
    subtitle.innerHTML = `<p>Current Weather</p>`;
    forecastCards.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Temperature: ${temperatureC}°C</h5>
          <p class="card-text">Description: ${description}</p>
        </div>
      </div>
    `;
  }

  // Fetch weather data when the page loads
  document.addEventListener('DOMContentLoaded', fetchWeatherData);

  // Optional: Add event listener for the search form
  document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const cityName = document.getElementById('city-name').value;
    // You can add logic here to fetch weather data for the searched city
    console.log('Searching for city:', cityName);
  });