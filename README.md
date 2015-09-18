# aashe-bulletin
The AASHE Bulletin - our newsletter

Uses [django-bulletin](http://github.com/aashe/django-bulletin)

## Installation

Install as you would any other package, but you must run
"./manage.py migrate django_constant_contact" immediately after
syncdb completes, or else migration of bulletin, first in the list,
will fail.

# Configuring Search.

Presently, we're using Whoosh as the backend for Haystack search.
For new installations, you'll need to initialize the Whoosh indexes
by:

    ./manage.py rebuild_index
