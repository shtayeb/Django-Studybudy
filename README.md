# Django project
Project Demo - [Study Buddy App Link](https://study-buddy-app.up.railway.app/)

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
python manage.py runserver --setting=core.settings.local # local settings
python manage.py runserver --setting=core.settings.production # production settings
```

## TODO

- [x] Email verification
- [x] Forgot password option
- [x] Code blocks in the rooms - should support markdown in messages inside room
- [x] Add new users to news room by default
- [x] style the flash messages
- [x] Soft delete for all models
- [x] Ability to join/leave a room
- [x] Ability to create private rooms(non members cant go to the room)
- [x] Room host can invite users to private rooms - (The added user will recieve notification and have the option to accept or reject the invite)
- [x] Make the invite user page into a modal pop up
- [x] Like/Dislike messages of a room by its participants

- Add message replies (Add Polymorphic relationship) [lnk](https://forum.djangoproject.com/t/get-all-children-of-self-referencing-django-model-in-nested-hierarchy/16761)
- Add room Admin

- Create infinite scroll in home and room page
- Create an autocomplete users list in the invite users to room page
- Fix Modal/Dialogs scrolls with page

- Account removal request, user is soft deleted and after one month its hard deleted and its room and message are set to null
- SEO meta tags for pages
- Add in markdown editor image upload

- Room admins can add/invite users to private rooms
- Ability to archive(block new messages) a room by admin
- Room participants management(Kick, Block and suspend participants of rooms by its Admin)
- Rooms message moderation by Admins

- Activity notification for joined rooms
- Glabal setting for notification settings
- Recaptcha for login on register page
- roles and permissions


## Docs

With django-extensions package, you access to these commands

>  `apt-get install graphviz`

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

msgs = Message.objects.filter(parent=None).annotate(fire_count=fire_count).annotate(like_count=like_count).annotate(poop_count=poop_count).prefetch_related(Prefetch("replies"))



## Installed Packages
- [django-easy-audit](https://github.com/soynatan/django-easy-audit)
- [django-extensions](https://github.com/django-extensions/django-extensions)
- [nplusone](https://github.com/jmcarp/nplusone)
- [django-debug-toolbar](https://)

## Packages to consider
- [django-prose](https://github.com/withlogicco/django-prose)
- [django-extra-settings](https://github.com/fabiocaccamo/django-extra-settings)
- [django-jet-reboot](https://github.com/assem-ch/django-jet-reboot)

- https://github.com/markdown-it/markdown-it