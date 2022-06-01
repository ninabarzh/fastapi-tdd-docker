# Test-Driven Development with FastAPI and Docker

Based on the awesome [Test-Driven Development with FastAPI and Docker](https://testdriven.io/courses/tdd-fastapi/)
 course, with a few changes:. 

* Management of python dependencies is done with`pyenv` and `poetry` (v2) instead of `pip`.
* Instead of the general Package registry with a [PAT](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#considering-cross-repository-access), the GitHub Container registry `ghcr.io` is used with the more secure `GITHUB_TOKEN`.

![Continuous Integration and Delivery](https://github.com/tymyrddin/fastapi-tdd-docker/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main)

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

```
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