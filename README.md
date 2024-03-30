## FavLinks : Django

*Step 1:
> Create environment
```
python3 -m venv .venv
source .venv/bin/activate
```

*Step 2:
> Install requirements
```
pip install -r requirements.txt
```

*Step 3:
> Create migrations
```
python manage.py makemigrations
```
> Apply migrations
```
python manage.py migrate
```

*Step 4:
> Start server
```
python manage.py runserver
```