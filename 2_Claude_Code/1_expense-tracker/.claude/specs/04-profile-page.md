# Spec: Profile Page

## Overview
Implement session-based authentication (login, logout) and a profile page so a signed-in user can see their account details. This step upgrades the existing stub `GET /login` route to handle `POST` and establish a Flask session, implements the `GET /logout` stub to clear that session, and implements the `GET /profile` stub to display the logged-in user's name, email, and member-since date. A `login_required` decorator is introduced so `/profile` (and future authenticated routes) can reject anonymous access. This closes the gap left by Step 03: the `login.html` template and form markup exist, but no session logic was ever wired into `app.py`, so there is currently no way to establish or check "logged in" state anywhere in the app.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, working `users` rows to log in with)

## Routes
- `GET /login` — render login form — public (already exists as stub, unchanged)
- `POST /login` — validate credentials, establish session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — logged-in
- `GET /profile` — render logged-in user's profile — logged-in

## Database changes
No new tables or columns. The existing `users` table (id, name, email, password_hash, created_at) covers all requirements.

No new DB helpers needed beyond what already exists — `get_db()` is used directly in `app.py` for a single `SELECT` by email (login) and by id (profile), consistent with how `create_user()` already isolates DB logic in `database/db.py`. Since these are simple lookups, add two small helpers to `database/db.py` to keep DB logic out of routes:
- `get_user_by_email(email)` — returns the user row (or `None`) matching the email, for login credential checks
- `get_user_by_id(user_id)` — returns the user row (or `None`) matching the id, for populating the profile page

## Templates
- **Modify:** `templates/login.html`
  - Confirm form `action` uses `url_for('login')` (currently hardcoded `/login` — must be fixed per CLAUDE.md rules)
  - Add a block to display a flashed error message (e.g. "Invalid email or password") using the existing `auth-error` style already present in the template
- **Modify:** `templates/base.html`
  - Nav links must reflect session state: show "Sign in" / "Get started" when logged out (current behavior); show a link to `/profile` and a "Log out" link (`url_for('logout')`) when logged in
- **Create:** `templates/profile.html`
  - Extends `base.html`
  - Displays the user's name, email, and "member since" date (formatted from `created_at`)
  - Follows the same card-based layout conventions as `auth-card` (reuse `--paper-card`, `--radius-md`, etc. from `style.css`)

## Files to change
- `app.py` — add session import, `login_required` decorator, upgrade `login()` to handle `POST`, implement `logout()`, implement `profile()`
- `database/db.py` — add `get_user_by_email()` and `get_user_by_id()` helpers
- `templates/login.html` — fix hardcoded form action, add flashed error display
- `templates/base.html` — conditionally render nav links based on session state

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies. Uses Flask's built-in `session` object and `werkzeug.security.check_password_hash` (werkzeug is already installed).

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Passwords hashed with werkzeug — use `check_password_hash` to verify on login, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs
- Store only `user_id` in the Flask session — never store the password hash or full user row in the session
- `login_required` must be implemented as a decorator in `app.py` (no new file) that checks `session.get("user_id")` and redirects to `url_for('login')` if absent
- `/profile` must use `login_required`
- On failed login (unknown email, or wrong password), flash a single generic error ("Invalid email or password") — never reveal whether the email exists
- On successful login, flash a welcome message and redirect to `url_for('profile')`
- `/logout` must clear the entire session (`session.clear()`) before redirecting
- Use `abort(405)` if an unsupported HTTP method reaches `/login`
- DB logic (the two new lookup helpers) belongs in `database/db.py`, never inline in `app.py`

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials on `/login` redirects to `/profile` and shows the correct user's name and email
- [ ] Submitting an unknown email or wrong password re-renders the login form with a generic "Invalid email or password" error, no session created
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in shows name, email, and member-since date for the correct user
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login`
- [ ] After logout, visiting `/profile` again redirects to `/login` (session is actually cleared)
- [ ] Nav bar shows "Sign in"/"Get started" when logged out, and profile/logout links when logged in
