sudo kill -9 $(sudo lsof -t -i:8000)
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py makemigrations authentication
python3 manage.py makemigrations question
python3 manage.py migrate
#python3 manage.py createsuperuser # uncomment when run first time
python3 manage.py runserver &