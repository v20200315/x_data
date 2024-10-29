# x_data
## some instructions
### github
#### git add.
#### git commit -m ""
#### git push -u origin main 
### django
#### python manage.py runserver
#### python manage.py makemigrations
#### python manage.py migrate
#### python manage.py startapp samples
#### python manage.py shell
#### python manage.py createsuperuser
### django celery
#### export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
#### celery -A x_data worker --loglevel=info
#### celery -A x_data beat --loglevel=info
### st url
#### https://victor-llm-sample.streamlit.app/
###
#### TRUNCATE TABLE stocks_stockhistorybfq, stocks_stockhistoryhfq, stocks_stockhistoryqfq RESTART IDENTITY CASCADE;