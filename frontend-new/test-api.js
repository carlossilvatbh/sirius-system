// Test script to verify API integration
console.log('Testing API integration...');

// Test basic fetch to backend
fetch('http://localhost:8001/estruturas/api/estruturas/')
  .then(response => {
    console.log('Backend response status:', response.status);
    return response.json();
  })
  .then(data => {
    console.log('Backend data received:', data.length, 'structures');
    console.log('First structure:', data[0]);
  })
  .catch(error => {
    console.error('Error fetching from backend:', error);
  });

// Test CORS
fetch('http://localhost:8001/estruturas/api/estruturas/', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3004'
  }
})
.then(response => {
  console.log('CORS test - Status:', response.status);
  console.log('CORS test - Headers:', response.headers);
})
.catch(error => {
  console.error('CORS test error:', error);
});

console.log('API tests initiated...');
