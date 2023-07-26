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
# Django packages
pip install -r requirements.txt

# npm packages
npm install
```

- Create `.env` file

```shell
cp .env.sample .env
```

- Migrate the database

```shell
python manage.py migrate
```

- Create a superuser

```shell
python manage.py createsuperuser
```

- Seed database with fake data 

```shell
python manange.py seed
```

- Run the server

```shell
python manage.py runserver --setting=core.settings.local # local settings
python manage.py runserver --setting=core.settings.production # production settings
```

- Run the vite server

```shell
npm run dev
```


## Docs
```python

class Product(models.Model):
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        limit_choices_to=
            {
                'model__in':('book','cupboard')
            }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')

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
- [x] Like/Dislike messages of a room by its members
- [x] Add message replies (Self referential) [Resource](https://forum.djangoproject.com/t/get-all-children-of-self-referencing-django-model-in-nested-hierarchy/16761)
- [x] Create infinite scroll in home page
- [X] Create an autocomplete users list in the invite users to room page
- [x] Add in markdown WYSGI editor 
- [x] Add vite for asset bundling
- [x] HTMX form and reactivity for adding new messages/replies
- [x] Add room Admin
- [x] Deactivate room message when unauthenticated
- [x] Create room settings page where admins can see all members, manage members, see invitations and its statuses, add new admins, invite users, edit room,
- [x] Room admins can add/invite users to private rooms
- [x] Ability to archive(block new messages) a room by admin/host(room.is_archived)
- [x] block room members
- [x] Room members management(Kick, Block and suspend members of rooms by its Admin)
- [x] Rooms message moderation by Admins
- [x] SEO meta tags for pages

- Automatically Create a meta tag banner for a room (use GET blog.shahryartayeb.com/generate_banner?text=Title)
- Account removal request, user is soft deleted
    - After one month its hard deleted and its room and message are set to null or to anonymous
    
- Recaptcha for login and register page

- Activity notification for joined rooms
- Glabal setting for notification settings
- roles and permissions




## Installed Packages
- [django-easy-audit](https://github.com/soynatan/django-easy-audit)
- [django-extensions](https://github.com/django-extensions/django-extensions)
- [nplusone](https://github.com/jmcarp/nplusone)
- [django-debug-toolbar](https://)

## Packages to consider
- [django-prose](https://github.com/withlogicco/django-prose)
- [django-extra-settings](https://github.com/fabiocaccamo/django-extra-settings)
- [django-jet-reboot](https://github.com/assem-ch/django-jet-reboot)
