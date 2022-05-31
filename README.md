# TDD FastAPI backend Docker files

Based on the awesome testdriven.io [Test-Driven Development with FastAPI and Docker](https://testdriven.io/courses/tdd-fastapi/)
 course (with a few changes). Management of python dependencies is done with Poetry (v2) instead.

### Build

In the repo root directory (where the `docker-compose.yml` is) build the containers with:

```bash
$ docker compose up -d --build
```

View container logs

```bash
$ docker compose logs web
```

Bring down and remove volumes:

```bash
$ docker compose down -v
```

### Database access

Access the database via `psql` with:

```bash
$ docker compose exec web-db psql -U postgres
```

Then connect to the database with:

```postgresql
postgres=# \c web_dev
postgres=# \dt
postgres=# \q
```

### Running tests

With the containers up and running, run the tests:

```bash
$ docker compose exec web python -m pytest
```

Coverage report:
```bash
$ docker compose exec web python -m pytest --cov="."
```

### Code quality

```bash
$ docker compose exec web black .
```

```bash
$ docker compose exec web flake8 .
```

```bash
$ docker compose exec web isort .
```