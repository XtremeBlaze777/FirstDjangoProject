# Google OAuth setup for new heroku deployment
1) Locally, run `python3 manage.py makemigrations`
2) On heroku bash, run the Site ID script with `chmod +x set_siteID.sh && ./set_siteID.sh`; add the printed SITE_ID in *LousListA8/settings.py*
3) Add the url of your heroku deployment to the *ALLOWED_HOSTS* variable in *LousListA8/settings.py*
4) Push to github/heroku
5) Reset your heroku database by going to *addons->postgres ->settings->reset database*
6) On heroku bash, create an admin account using `python3 manage.py createsuperuser`
7) Login to your admin from the */admin* url of your deployment
8) Do Step 5 of https://www.section.io/engineering-education/django-google-oauth/ to set up google OAuth like normal:
    - Go to the social sites section and make sure the only url is the current heroku deployment.
    - Go to the social apps section and add an app that has Google as the provider, and get the rest of the fields from our google developer console
9) Add the url (and callback url) of your heroku deployment to the Google Developer Console
10) On heroku bash run `python3 manage.py seed`



## Citations
* Title: Django documentation\
Code version: 4.1\
Software License: BSD 3-Clause\
URL: https://docs.djangoproject.com/en/4.1/
* Title: User Registration in Django using Google OAuth\
Author: Geoffrey Mungai _(Author)_, Adrian Murage _(Contributer)_ \
Date: Dec. 18, 2020\
URL: https://www.section.io/engineering-education/django-google-oauth/
* Title: Real-time Chat Messenger\
Author: Mitch Tabian\
Date: Aug. 2, 2021\
URL: https://codingwithmitch.com/courses/real-time-chat-messenger/
* Title: Django Tutorials\
Author: William Vincent\
Date: Mar. 22, 2022\
URL: https://learndjango.com/
* Title: Jinja\
Code version: 3.1\
URL: https://jinja.palletsprojects.com/en/3.1.x/

* Various StackOverflow Links:
    - https://stackoverflow.com/questions/57283470/django-pip-install-django-herokupsycopg2-error-is-blocking-deployment-to-her
    - https://stackoverflow.com/questions/15409366/django-socialapp-matching-query-does-not-exist
    - https://stackoverflow.com/questions/21084806/finding-the-site-id-of-a-site-in-django-admin
    - https://stackoverflow.com/questions/769683/postgresql-show-tables-in-postgresql
    - https://stackoverflow.com/questions/26276397/django-1-7-upgrade-error-appregistrynotready-apps-arent-loaded-yet
    - https://stackoverflow.com/questions/4847469/use-django-from-python-manage-py-shell-to-python-script
    - https://stackoverflow.com/questions/25386119/whats-the-difference-between-a-onetoone-manytomany-and-a-foreignkey-field-in-d
    - https://stackoverflow.com/questions/902034/how-can-i-check-the-size-of-a-collection-within-a-django-template