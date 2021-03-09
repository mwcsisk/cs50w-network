from django.db.models import Count, Exists, OuterRef
from .models import User, Post
from django.core.paginator import Paginator

def get_posts(request,username=False,users=False,per_page=10):
    """Function to retrieve posts from the database and annotate the number of likes.
    Also annotates if the current user liked the post. Returns a Paginator object.

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
    if request.user.is_authenticated:
        posts = posts.annotate(liked=Exists(request.user.liked.filter(id=OuterRef('pk'))))
    return Paginator(posts.annotate(num_likes=Count('likes')).order_by('-timestamp'), per_page)

def get_page_number(request, default=1):
    """Function to get a page number that is always an integer from a GET request.
    Takes the current request.
    
    Parameters:
    default (int) - The default to fall back to if converting to an integer fails. Default is 1.
    """

    page_num = request.GET.get('page', default=default)

    try:
        return int(page_num)
    except ValueError:
        return default