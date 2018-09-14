RE: upgrading to Django 1.10 (and native JSONField).

See https://stackoverflow.com/questions/41683385/how-should-i-upgrade-from-bradjaspers-django-jsonfield-to-djangos-built-in-jso#

Can't just install new code and run migrations.  Need to do this dance.

(Or do I?)

Steps:

Add the new Postgres JSON field named json_new.

Delete the old field. Delete the old import.

Make migrations, migrate.

Rename new field to old field name. json_new > json.

Make migrations, migrate.

Done.
