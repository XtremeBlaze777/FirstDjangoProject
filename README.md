## Google OAuth setup for new heroku deployment
1) Run a bash shell on your heroku deployment (either using the Heroku CLI or from the Heroku Website)
2) Create an admin account using `python3 manage.py createsuperuser`
3) Login to your admin by from the */admin* url of your deployment
4) Go to the social sites section and make sure the only url is the current heroku deployment
5) Go to the social apps section and add an app that has Google as the provider, and get the rest of the fields from our google developer console
6) Add the url of your heroku deployment to the ALLOWED_HOSTS variable
7) Add the url (and callback url) of your heroku deployment to the Google Developer Console
