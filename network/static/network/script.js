document.addEventListener('DOMContentLoaded', function() {
    
    // Add post functionality
    let newPostForm = document.querySelector('#new-post');

    if (newPostForm) {
        newPostForm.onsubmit = () => {

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
            });

            return false;
        };
    };

    let followButton = document.querySelector('#follow-button')

    if (followButton) {
        followerCount = document.querySelector('#follower-count');

        followButton.onclick = () => {
            if (followButton.innerHTML.trim() === 'Follow') {
                updateFollowing('follow', followButton.value)
                .then(() => {
                    followButton.innerHTML = 'Unfollow';
                    let newCount = parseInt(followerCount.innerHTML) + 1;
                    followerCount.innerHTML = newCount;
                });
            } else {
                updateFollowing('unfollow', followButton.value)
                .then(() => {
                    followButton.innerHTML = 'Follow'
                    let newCount = parseInt(followerCount.innerHTML) - 1;
                    followerCount.innerHTML = newCount;
                });
            };
        };
    };

    let editButtons = document.querySelectorAll('.edit-button')

    if (editButtons) {
        editButtons.forEach(element => {
            element.onclick = () => {
                let postBox = document.querySelector(`#post-${element.value}-body`);
                let postBody = postBox.innerHTML.trim();
                postBox.innerHTML = '';
                postBox.insertAdjacentElement('afterbegin', newEditForm(element.value, postBody));
                element.disabled = true;
            };
        });
    };
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

async function updateFollowing(action, followee) {
    // Function to update the "following" status for a user
    // Takes an action (either 'follow' or 'unfollow') and the username being followed/unfollowed
    await fetch('/api/follow', {
        method: 'PUT',
        body: JSON.stringify({
            action: action,
            followee: followee
        })
    });
}

function newEditForm(postId, postBody) {
    // Function to generate HTML for an edit form
    form = document.createElement('form');
    form.innerHTML = `
    <div class="form-group">
        <textarea id="post-${postId}-edit-body" class="form-control" rows="3">${postBody}</textarea>
    </div>
    <button type="submit" class="btn btn-primary">Save</button>`;
    form.onsubmit = () => {
        const newPostBody = document.querySelector(`#post-${postId}-edit-body`)
        fetch(`/api/post/edit`, {
            method: 'POST',
            body: JSON.stringify({
                body: newPostBody.value,
                post: postId
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                console.log(result.error)

                return false;
            }
            document.querySelector(`#post-${postId}-body`).innerHTML = result.body;
            document.querySelector(`#post-${postId}-edit-button`).disabled = false;

        })
        
        return false;
    }
    return form;
}