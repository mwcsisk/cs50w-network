# cs50w-network
My code for [Project 4 of CS50W](https://cs50.harvard.edu/web/2020/projects/4/network/).

## Installation
If you're interested in running my code on your local machine, you'll first need to install [Python](https://www.python.org/) and [Django](https://www.djangoproject.com/). You may also need to install SQLite3, though I'm pretty sure Django ships with that.

Once you do, follow these steps:

1. In a terminal navigated to whatever folder you downloaded my code into, run `python manage.py makemigrations network`
2. Run `python manage.py migrate`
3. Run `python manage.py runserver` to run the server.

That should be it, since this isn't production code there's no need for keys and I'm not using any outside APIs.