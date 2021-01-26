document.addEventListener('DOMContentLoaded', function() {
    
    // Add post functionality
    document.querySelector('#new-post').onsubmit = () => {

        // Add post to database
        fetch('/api/post', {
            method: 'POST',
            body: JSON.stringify({
                body: document.querySelector('#new-post-body').value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })

        return false;
    }
});