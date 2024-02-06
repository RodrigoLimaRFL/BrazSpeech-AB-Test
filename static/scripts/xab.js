// function to read the audio submitted by the user
function handleSubmit(event) {
    event.preventDefault();

    let selectedAudio = document.querySelector('input[name="radio-group"]:checked').id;
    console.log(JSON.stringify({ selectedAudio }));

    fetch('/xab', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedAudio }),
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server
        console.log(data);
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            alert("ERROR WITH GRADE SUBMISSION");
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("send-button").addEventListener("click", handleSubmit);
});