# Django project
Project Demo - [Study Buddy App Link](https://study-buddy-app.up.railway.app/)

Project Kanban - [Consider Contributing](https://github.com/users/shtayeb/projects/1)

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


## Installed Packages
- [django-easy-audit](https://github.com/soynatan/django-easy-audit)
- [django-extensions](https://github.com/django-extensions/django-extensions)
- [nplusone](https://github.com/jmcarp/nplusone)
- [django-debug-toolbar](https://)

## Packages to consider
- [django-prose](https://github.com/withlogicco/django-prose)
- [django-extra-settings](https://github.com/fabiocaccamo/django-extra-settings)
- [django-jet-reboot](https://github.com/assem-ch/django-jet-reboot)
