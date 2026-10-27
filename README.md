# Testr — Back End

REST API for **Testr**, an exam question-bank platform. Teachers add past-paper questions (organised by discipline, subject, paper and topic tag), reviewers verify them, and students/teachers browse and filter the bank to build tests.

This is the Django REST Framework service consumed by the [Testr front end](https://github.com/Gladiathor1/Testr_Frontend).

## Features

- **Accounts** — registration with email verification, JWT login/refresh/logout, password reset by email
- **Social login** — Google and Facebook
- **Roles** — regular users, teachers (`is_teacher`) and reviewers (`is_reviewer`)
- **Question bank** — disciplines, subjects, papers (year / session / code), tags, questions with rich-text answers, difficulty and type, and attached question/answer images
- **Review workflow** — questions start as *In review* and are approved by a verifier
- **Bulk import** — upload papers and tags from CSV files
- **API docs** — Swagger UI and ReDoc generated with drf-yasg

## Tech stack

- Python 3, Django 3.2, Django REST Framework
- Simple JWT, django-allauth / dj-rest-auth, Google & Facebook SDKs
- MySQL
- django-ckeditor (rich text), django-versatileimagefield (images)
- drf-yasg (OpenAPI docs), django-cors-headers

## Project structure

```
testr_services/  Django project settings & root URLs
authentication/  Custom User model, register/login/verify/reset endpoints
social_auth/     Google & Facebook login
question/        Question-bank models, serializers, viewsets, CSV import
template/        Simple HTML pages (CSV upload forms, success page)
admin/           Separate scaffold Django project (not used by the API)
run.sh           Migrate and start the dev server
```

## API

All routes are prefixed with `/testr-api/`.

| Path | Description |
| --- | --- |
| `swagger-ui/`, `redoc/` | Interactive API documentation |
| `admin/` | Django admin |
| `auth/register/`, `auth/login/`, `auth/logout/` | Account management |
| `auth/email-verify/` | Email verification link |
| `auth/token/refresh/` | Refresh a JWT |
| `auth/request-reset-email/`, `auth/password-reset/<uidb64>/<token>/`, `auth/password-reset-complete` | Password reset flow |
| `social/google/`, `social/facebook/` | Social login |
| `engine/disciplines/`, `engine/subjects/`, `engine/papers/`, `engine/tags/` | Taxonomy CRUD (DRF router) |
| `engine/questions/` | Question CRUD |
| `engine/myquestions/` | Questions created by the current user |
| `engine/images/` | Question/answer images |
| `engine/review/` | Verifier endpoints for approving questions |
| `engine2/upload/csv/`, `engine2/upload/tags/` | Bulk CSV import |
| `engine2/disciplines`, `subjects`, `papers`, `questions`, `tags` | Filterable list endpoints |

## Getting started

### Prerequisites

- Python 3.9+
- MySQL 8 and the MySQL client development headers (`libmysqlclient-dev` on Ubuntu)

### Setup

```bash
pip install -r requirements.txt
```

Create a database and user (see `installations.txt` for the full Ubuntu setup), then update `DATABASES`, `SECRET_KEY`, the email settings and the social-auth credentials in `testr_services/settings.py`. Prefer loading these from environment variables rather than committing them.

### Run

```bash
python manage.py makemigrations authentication question
python manage.py migrate
python manage.py createsuperuser   # first run only
python manage.py runserver
```

or simply `sh run.sh`. The API is then available at `http://127.0.0.1:8000/testr-api/` and the docs at `http://127.0.0.1:8000/testr-api/swagger-ui/`.
