# Server Inventory & Incident Tracker

A Django web application for tracking servers and logging incidents: who owns a server, what state it is in, what problems it has had, and who is handling them.

This is a learning project. It was built to get hands-on practice with Django models and migrations, the ORM, authentication, and access control.

## Project Status

Work in progress.

- [x] Data models: servers, tags, incidents, comments
- [x] User registration, login, and logout
- [x] Server pages: list, detail, create, edit, delete
- [x] Access control (Django groups and permissions)
- [ ] Incident pages
- [ ] Comments on the incident page
- [ ] Filtering and search in lists

## Features

- **Authentication.** Registration, login, and logout. A new user is signed in automatically after registering.
- **Server inventory.** Hostname, IP address, OS, status (active / maintenance / decommissioned), owner, and tags. When a server is created, the current user automatically becomes its owner.
- **Incident tracking.** Each incident is linked to a server and has a severity (low / medium / high / critical), a status (open / in_progress / resolved), an optional assignee, creation and resolution timestamps, and comments.
- **Access control.** Anonymous visitors are redirected to the login page. Any signed-in user can view data, but adding, editing, and deleting requires the corresponding permission.
- **Django admin.** Manage users, groups, and data.

## Tech Stack

- Python 3.12+ (developed on 3.13)
- Django 6.1
- SQLite
- Django templates (HTML), built-in authentication and permissions system

## Data Model

| Model | Fields |
|---|---|
| `Tag` | `name` (unique) |
| `Server` | `hostname` (unique), `ip_address`, `os`, `owner` → User, `status`, `tags` ↔ Tag, `created_at` |
| `Incident` | `server` → Server, `title`, `description`, `severity`, `status`, `assignee` → User (nullable), `created_at`, `resolved_at` |
| `IncidentComment` | `incident` → Incident, `author` → User, `text`, `created_at` |

**Data integrity:**

- `Server.hostname` and `Tag.name` are unique.
- A database-level `CheckConstraint` requires `resolved_at` to be set whenever an incident's status is `resolved`.
- Deletion behavior: a server owner or a comment author cannot be deleted while records still reference them (`PROTECT`). Deleting a server deletes its incidents, and deleting an incident deletes its comments (`CASCADE`). Deleting an assignee keeps the incident and clears its `assignee` field (`SET_NULL`).

**Indexes and ordering:**

- `Server`: index on `(status, hostname)`, ordered by `hostname`.
- `Incident`: indexes on `(status, severity)` and `(server, -created_at)`, ordered newest first.
- Every foreign key has a `related_name` (for example, `server.incidents` and `user.servers`), and every model defines `__str__`.

## Access Control

| Who | What they can do |
|---|---|
| Anonymous visitor | Sees only the login and registration pages; everything else redirects to login |
| Signed-in user (no extra permissions) | Views the server list and server detail pages |
| Member of a group with `add_server` / `change_server` | Additionally creates and edits servers |
| User with `delete_server` | Deletes servers |
| Superuser | Everything |

Permissions are enforced in the views (`LoginRequiredMixin`, `PermissionRequiredMixin`), not just by hiding buttons in templates: opening a restricted URL directly without the required permission returns a 403 error.

## Project Structure

```
backend_project/
├── manage.py
├── requirements.txt
├── config/          # project settings and root URLs
├── accounts/        # registration, login, logout
├── inventory/       # Server and Tag models, server pages
├── incidents/       # Incident and IncidentComment models
└── templates/       # base.html, forms, login and server templates
```

## Quick Start

```bash
git clone https://github.com/TouchMeda/Backend_project.git
cd Backend_project

python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The app will be available at http://127.0.0.1:8000/.

### Granting Permissions

1. Open `/admin/` and sign in as a superuser.
2. Under **Groups**, create a group such as `Operators` and select the permissions `inventory | server | Can add server` and `Can change server`.
3. Under **Users**, add the desired user to that group.

## What This Project Covers

- Django models: `TextChoices`, `Meta` (`ordering`, `indexes`, `constraints`), `related_name`, `on_delete`, ForeignKey and ManyToMany relations.
- Migrations: the `makemigrations` → `sqlmigrate` → `migrate` workflow and inspecting the generated SQL.
- ORM: filtering, reverse relations, `select_related` / `prefetch_related`.
- Class-based views: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.
- Authentication and authorization: registration, login, logout, groups and permissions, access mixins.
- Templates: inheritance (`base.html`), CSRF protection in forms, permission checks in templates.

## Important

This is a learning project. `DEBUG` is enabled and `SECRET_KEY` was auto-generated, so the project is not suitable for public deployment as it stands.
