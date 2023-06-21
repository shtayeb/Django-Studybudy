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
- [x] Code blocks in the rooms - should support markdown in messages inside room
- Recaptcha for login an register page
- Email verification
- Create an event and its listner
- Forgot password option
- roles and permissions
- style the flash messages 
