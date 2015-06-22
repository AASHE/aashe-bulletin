# aashe-bulletin
The AASHE Bulletin - our newsletter

Uses [django-bulletin](http://github.com/aashe/django-bulletin)

# Configuring Search.

Presently, we're using Whoosh as the backend for Haystack search.
For new installations, you'll need to initialize the Whoosh indexes
by:

    ./manage.py rebuild_index
