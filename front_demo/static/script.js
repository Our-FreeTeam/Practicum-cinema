document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission

  // Get the values entered by the user
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;

  // Create the data object to be sent to the server
  var data = {
    user: username,
    password: password
  };

  // Send a POST request to the server
  fetch('http://localhost:8001/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    console.log(response.headers.get('access_token'))
    console.log(response.headers.keys())
    if (response.ok) {
      // Extract the access_token and refresh_token from the response headers
      var access_token = response.headers.get('access_token');
      var refresh_token = response.headers.get('refresh_token');

      // Set the access_token and refresh_token as headers for the subsequent requests
      var headers = {
        'access_token':  access_token,
        'Refresh-Token': refresh_token
      };

      // Redirect the user to the dashboard page and pass the headers as query parameters
      var url = new URL('dashboard.html', window.location.href);
      url.searchParams.append('access_token', access_token);
      url.searchParams.append('refresh_token', refresh_token);

      window.location.href = url.href;
    } else {
      // Display an error message if login fails
      document.getElementById('errorMessage').textContent = 'Invalid username or password';

      // Display the server's error message above the form
      response.json().then(data => {
        var errorMessage = '';
        if (Array.isArray(data)) {
          errorMessage = data.map(error => error.msg).join(' ');
        } else {
          errorMessage = JSON.stringify(data);
        }
        document.getElementById('serverErrorMessage').textContent = errorMessage;
      });
    }
  })
  .catch(error => {
    // Display an error message if an error occurs
    document.getElementById('errorMessage').textContent = 'An error occurred while making the request.';
    console.error('Error:', error);
  });
});
