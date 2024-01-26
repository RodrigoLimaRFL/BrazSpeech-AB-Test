class loginCredential {
    constructor(username, password) {
        this.username = username;
        this.password = password;
    }
}

/*let credentials;

fetch("/read_json")
    .then(response => {
        if (!response.ok){ 
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })
    // After reading the JSON file, create an array of login credentials
    .then(data => {
        let accounts = data.accounts;
        credentials = new Array();
        for(let i = 0; i < accounts.length; i++){
            credentials.push(new loginCredential(accounts[i].username, accounts[i].password));
        }
        console.log(credentials);
    })
    .catch(err => console.log(err));
*/

// Function to handle the login form submission
function handleSubmit(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data);
        if (data.success) {
            // Redirect or perform other actions based on the response
            window.location.href = data.redirect;
        } else {
            // Show an alert for unsuccessful login
            alert("Invalid username or password");
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    form.addEventListener("submit", handleSubmit);
});