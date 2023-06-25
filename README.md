# Django project

## Getting Started

- Clone the repo

```shell 
git clone https://github.com/shtayeb/Django-Studybudy-YT.git
```

- Create a virtualenv

```shell
virtualenv .venv
```

- Activate the virtualenv

```shell
source ./.venv/bin/activate
```

- Install requirements

```shell
pip install -r requirements.txt
```

- Migrate the database

```shell
python manage.py migrate
```

- Create a superuser

```shell
python manage.py createsuperuser
```

- Run the server

```shell
python manage.py runserver
```
## TODO
- [x] Email verification
- [x] Forgot password option
- [x] Code blocks in the rooms - should support markdown in messages inside room
- [x] Add new users to news room by default
- style the flash messages 
- Recaptcha for login an register page
- roles and permissions


## Docs
With django-extensions package, you access to these commands
Install ``` apt-get install graphviz ```

```shell
# List all you app urls
python manage.py show_urls

# Generate ERD of all you DB tables
python manage.py graph_models -a -o myapp_models.png

# Generate ERD of specific apps
python manage.py graph_models base auth -o myapp_models.png

python manage.py shell_plus
python manage.py shell_plus --print-sql

python manage.py list_model_info --model base.Room

python manage.py list_signals 

python manage.py  reset_db mybucket

python manage.py admin_generator <your_app_name>

```