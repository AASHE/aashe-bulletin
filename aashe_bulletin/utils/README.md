# Dumping history

We dump history out of Drupal and Drupal gives is to us as a big HTML
table. To ease loading, we convert the HTML into a CSV file.

0. Dump stories.

  <http://www.aashe.org/exports/bulletin_dump_stories>

  Will download as `bulletin_dump_stories`.

0. Dump events.

  <http://www.aashe.org/exports/bulletin_dump_events>

  Will download as `bulletin_dump_events`.

0. Dump jobs.

  <http://www.aashe.org/exports/bulletin_dump_jobs>

  Will download as `bulletin_dump_jobs`.

0. Convert to CSV.

        ~/bin/table2csv < bulletin_dump_stories > bulletin_dump_stories.csv
        ~/bin/table2csv < bulletin_dump_events > bulletin_dump_events.csv
        ~/bin/table2csv < bulletin_dump_jobs > bulletin_dump_jobs.csv

0. mv where the loaders look:

        mv bulletin_dump_stories.csv $BULLETIN_ROOT/bulletin/utils/dumps/
        mv bulletin_dump_events.csv $BULLETIN_ROOT/bulletin/utils/dumps/
        mv bulletin_dump_jobs.csv $BULLETIN_ROOT/bulletin/utils/dumps/

# Loading initial data, including history

0. You gotta have the categories before Posts, so run
  `.seed_categories.main`.

0. Run `.load_issue_templates.main`. In addition to the default AASHE Issue
   Template, this will create the AASHE Bulletin Newsletter.

0. Run `.load_dumped_jobs.main`.

0. Run `.load_dumped_events.main`.

0. Run `.load_dumped_stories.main`.

0. Run `.load_ad_sizes.main`.
