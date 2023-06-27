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
- [x] style the flash messages
- [x] Soft delete for all models
- Ability to join/leave a room
- Add message replies (Add Polymorphic relationship)
- SEO meta tags for pages
- Account removal request
- Add in markdown editor image upload
- Add room Admin
- Ability to archive(block new messages) a room by admin
- Ability to create private rooms
- Room participants management(Kick, Block and suspend participants of rooms by its Admin)
- Rooms message moderation by Admins
- Like/Dislike messages of a room by its participants
- Activity notification for joined rooms
- Glabal setting for notification settings
- Recaptcha for login on register page
- roles and permissions

## Docs

With django-extensions package, you access to these commands
Install `apt-get install graphviz`

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



```shell
git commit -m "The wrong commit message"

# Edit the last commit message
git commit --amend -m "This is the right commit message"
```

## Packages to Install
[django-prose](https://github.com/withlogicco/django-prose)
[django-extra-settings](https://github.com/fabiocaccamo/django-extra-settings)