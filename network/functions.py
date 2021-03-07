from django.db.models import Count
from .models import User, Post

def get_posts(username=False):
    """Function to retrieve posts from the database and annotate the number of likes.

    Parameters:
    username (str) - Use to retrieve only posts from a specific user (optional)
    """
    
    if username:
        posts = User.objects.get(username=username).posts.all()
    else:
        posts = Post.posts.all()
    return posts.annotate(num_likes=Count('likes')).order_by('-timestamp')