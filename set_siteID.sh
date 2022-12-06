#!/bin/bash
echo 'Enter the name of your heroku app (ex: mysite.herokuapp.com): '
read APP_NAME
DJANGO_SITEID=$(python3 ./site_id.py $APP_NAME)
echo $DJANGO_SITEID
