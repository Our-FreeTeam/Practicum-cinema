window.addEventListener('DOMContentLoaded', function() {
  console.log('Page loaded');  // Log the page load event

  var queryString = window.location.search;
  var urlParams = new URLSearchParams(window.location.search);
  let cookies = document.cookie.split("; ");
  alert(cookies)
  let access_token_cookie = cookies.find(row => row.startsWith("access_token"));
  let access_token = access_token_cookie ? access_token_cookie.split('=')[1] : null;

  // Retrieve the user ID
  fetch('http://localhost:8001/v1/auth/get_my_id', {
    method: 'GET',
    headers: {
        'access_token': access_token
    }
  })
  .then(response => {
    console.log('User ID response:', response);  // Log the user ID response
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to retrieve user ID');
    }
  })
  .then(data => {
    var userId = data.user_id;
    console.log('User ID:', userId);  // Log the user ID

    // Get the current date and calculate the end date for the subscription
    var startDate = new Date().toISOString();
    var endDate = new Date();
    endDate.setDate(endDate.getDate() + 30);
    endDate = endDate.toISOString();

    console.log('Start Date:', startDate);  // Log the start date
    console.log('End Date:', endDate);  // Log the end date

    // Payment request data
    var paymentData = {
      user_id: userId,
      start_date: startDate,
      end_date: endDate,
      subscription_type_id: null,  // Set the correct subscription type ID
      is_active: true,
      is_repeatable: true,
      save_payment_method: true
    };

    console.log('Payment Data:', paymentData);  // Log the payment data

    document.getElementById('payButton').addEventListener('click', function() {
      console.log('Pay Button clicked');  // Log the pay button click event

      // Send payment request
      fetch('http://localhost:8200/api/v1/subscriptions/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'access_token': access_token,
        },
        body: JSON.stringify(paymentData)
      })
      .then(response => {
        console.log('Payment response:', response);  // Log the payment response
        if (response.ok) {
          document.getElementById('paymentMessage').textContent = 'Payment successful!';
        } else {
          throw new Error('Payment failed');
        }
      })
      .catch(error => {
        document.getElementById('paymentMessage').textContent = 'An error occurred while processing the payment.';
        console.error('Error:', error);
      });
    });
  })
  .catch(error => {
    document.getElementById('paymentMessage').textContent = 'Failed to retrieve user ID.';
    console.error('Error:', error);
  });
});
