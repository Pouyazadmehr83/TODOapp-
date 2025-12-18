# Todo App (Django)

Modern task manager built with Django 6 and Bootstrap. The project showcases authenticated CRUD operations, filtering UX, and dashboard-style UI components that fit nicely in a portfolio/resumé.

## Highlights

- **Authentication ready** – leverages Django's auth system to scope every task to the signed-in user.
- **Task CRUD** – create, read, update, delete with CSRF-protected forms and inline validation feedback.
- **Search & filtering** – query tasks by keyword, status, priority, and weekday via a responsive filter bar.
- **Weekly planner view** – quick-access weekday buttons plus colored cards (green/yellow/red) that reflect priority.
- **Mark as done** – single-click actions from both the list and details views; completed items broadcast success messages.
- **Pagination** – server-side pagination keeps large task lists fast (6 items per page with navigation controls).
- **Flash messages** – consistent user feedback for every action (create, update, delete, mark done).
- **Responsive UI** – Bootstrap 4 base template with reusable navbar, forms, and alert components.

## Tech Stack

- Python 3.13
- Django 6.0
- Bootstrap 4 (CDN)
- SQLite (default dev database)

## Running Locally

```bash
poetry install  # or pip install -r requirements.txt if you prefer
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in via the default Django authentication flow.

## Feature Tour

### Dashboard (`/`)
- Weekly buttons filter tasks by the `day_of_week` stored on each task.
- Search box filters by title/description; dropdowns filter by status (Done/Pending) and priority (Low/Medium/High).
- Colored cards highlight priority while showing due date, weekday, and quick action buttons.
- Inline buttons/forms support edit, delete, and mark-as-done flows without leaving the page.
- Pagination widgets preserve all active filters while browsing.

### Task Details (`/details/<id>/`)
- Full description, metadata (priority, weekday, due date, timestamps).
- Action buttons plus confirmation form for delete and a radio toggle for marking completion.

### Task Form (`/create/`, `/details/<id>/edit/`)
- Shared Bootstrap form with server-side validation errors rendered inline.
- Includes fields for title, notes, due date, weekday, priority, and completion flag.

## Messaging & Feedback

- Django's message framework is wired to every mutating action.
- Base template renders dismissible Bootstrap alerts so users get confirmation immediately.

## Resume Angle

Use this project to demonstrate:
1. Django proficiency (views, forms, models, auth, pagination, messages).
2. UX attention to detail (filtering, search, color-coded priority, responsive cards).
3. Secure multi-user design (task ownership enforced at every endpoint).

Feel free to fork/customize the styling or deploy it as part of your portfolio.
