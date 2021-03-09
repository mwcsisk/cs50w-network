from django.db.models import Count
from .models import User, Post

def get_posts(username=False,users=False):
    """Function to retrieve posts from the database and annotate the number of likes.

    Parameters:
    username (str) - Use to retrieve only posts from a specific user (optional)
    users (QuerySet) - Use to retrieve only posts from a set of users (optional)
    """
    
    if username and users:
        raise ValueError('Either a username or a set of users can be specified, but not both')
    elif username:
        posts = User.objects.get(username=username).posts.all()
    elif users:
        posts = Post.posts.filter(author__id__in=users)
    else:
        posts = Post.posts.all()
    return posts.annotate(num_likes=Count('likes')).order_by('-timestamp')