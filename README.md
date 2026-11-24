Tracking of servers and incidents. Django, SQLite.



How to launch:

bash

git clone git@github.com:YOUR_LOGIN/django-inventory.git

cd Backend_project

python3 -m venv venv && source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
​
