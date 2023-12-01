.PHONY: install
install:
	poetry install

.PHONY: lint
lint:
	ruff check --output-format=github ./src && ruff format ./src

.PHONY: migrate
migrate:
	poetry run python src/manage.py migrate

.PHONY: migrations
migrations:
	poetry run python src/manage.py makemigrations

.PHONY: serve
serve:
	poetry run python src/manage.py runserver

.PHONY: vite
vite:
	cd src && npm run dev

.PHONY: npm-install
npm-install:
	cd src && npm install

.PHONY: npm-build
npm-build:
	cd src && npm run build

.PHONY: superuser
superuser:
	poetry run python src/manage.py createsuperuser

.PHONY: update
update: install migrate;

.PHONY: test
test:
	cd src && poetry run python manage.py test

.PHONY: db-seed
db-seed:
	poetry run python src/manage.py seed 