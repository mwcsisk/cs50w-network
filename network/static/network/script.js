document.addEventListener('DOMContentLoaded', function() {
    
    // Add post functionality
    document.querySelector('#new-post').onsubmit = () => {

        // Set up elements we need
        const body = document.getElementById('new-post-body');
        const message = document.getElementById('new-post-feedback');
        const form = document.getElementById('new-post');
        
        // Add post to database
        fetch('/api/post', {
            method: 'POST',
            body: JSON.stringify({
                body: body.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            
            // Check for errors
            if (result.error) {
                body.classList.add('is-invalid');
                
                message.className = 'invalid-feedback';
                message.innerHTML = result.error;
                
                return false;
            }
            
            form.classList.add('was-validated');
            // Display success message to user
            body.classList.remove('is-invalid');
            body.classList.add('is-valid');
            message.className='valid-feedback';
            message.innerHTML = 'Post successfully created!';

            // Add new post to posts view
            renderPost('afterbegin', result);

            // Clear post form body
            document.getElementById('new-post-body').value = '';
        })

        return false;
    }
});

function renderPost(position, postData) {
    // Function to render posts to the posts view
    // Takes a positional argument and the data for the actual post
    const newPost = document.createElement('div');
    newPost.className = 'post-box';
    newPost.innerHTML = `
        <div class="row justify-content-between">
            <div class="col-md-auto author"><a href="/user/${postData.author}">${postData.author}</a></div>
            <div class="col-md-auto edit-link">
                Edit
            </div>
        </div>
        <div class="body">
            ${postData.body}
        </div>
        <div class="timestamp">
            ${postData.timestamp}
        </div>
        <div class="likes">
            Likes: ${postData.num_likes}
        </div>
        `;
    const view = document.querySelector("#posts-view");
    view.insertAdjacentElement(position, newPost);
}

function updateFollowing(action, followee) {
    // Function to update the "following" status for a user
    // Takes an action (either 'follow' or 'unfollow') and the username being followed/unfollowed
    fetch('/api/follow', {
        method: 'PUT',
        body: JSON.stringify({
            action: action,
            followee: followee
        })
    })
}