There are some funky things going on with database conflicts so you need to do these things to get
postgres and sqlite working

Before Deploying:
Reset the postgres database by going to addons->postgres ->settings -> reset database

After Deploying:
1. go to the heroku bash and do 'python3 manage.py createsuperuser' to set up admin

2. Now do Step 5 of https://www.section.io/engineering-education/django-google-oauth/ to set up google OAuth like normal


3.Now it's time to fuss with the Site_id... go back to heroku bash and do the following commands
python3 manage.py shell
>>> from django.contrib.sites.models import Site
>>> site = Site.objects.get(name="project-a-08-test.herokuapp.com")
>>> site.id     - (SET THE SITE_ID TO THIS VALUE)

 

4.Go back to the heroku bash/ command line and enter the following commands

 4a: 'python3 manage.py makemigrations'
 4b: 'python3 manage.py migrate'
 4c: 'python3 manage.py seed'   This one takes a while as it is loading the models from the api into the database