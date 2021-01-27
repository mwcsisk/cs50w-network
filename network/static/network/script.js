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

            // Add new post to posts view
            let newPost = document.createElement('div');
            newPost.className = 'post-box';
            newPost.innerHTML = `
            <div class="row justify-content-between">
                <div class="col-md-auto author">${result.author}</div>
                <div class="col-md-auto edit-link">
                    Edit
                </div>
            </div>
            <div class="body">
                ${result.body}
            </div>
            <div class="timestamp">
                ${result.timestamp}
            </div>
            <div class="likes">
                Likes: ${result.num_likes}
            </div>
            `;
            const view = document.querySelector("#posts-view");
            view.insertAdjacentElement('afterbegin', newPost);
        })

        return false;
    }
});