# Spec: Login and Logout

## Overview
Implement session-based authentication for Spendly: users sign in with email and password on the existing `/login` stub, and can sign out via the existing `/logout` stub. On successful login, the user's identity is stored in the Flask session so later steps (profile, expenses) can identify the current user. This is the second half of the auth flow started in Step 02 — registration created accounts, this step lets users actually use them.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, working `/register` flow, users exist with hashed passwords)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade it)
- `POST /login` — verify credentials, start session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/login` — logged-in

## Database changes
No new tables or columns. A new read helper must be added to `database/db.py`:
- `get_user_by_email(email)` — returns the user row (id, name, email, password_hash) matching the given email, or `None` if not found. Parameterised query only.

## Templates
- **Modify:** `templates/login.html`
  - Change the form `action` to `url_for('login')` with `method="post"` (currently hardcoded to `/login`)
  - Add `name` attributes already present on inputs (`email`, `password`) — confirm they match what the route reads via `request.form.get()`
  - Flash error display already exists via `base.html`'s shared flash block — remove the unused local `{% if error %}` block in favor of the shared flash messages
  - Keep all existing visual design

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST` with session logic; replace the `logout()` stub with real session-clearing logic
- `database/db.py` — add `get_user_by_email()` helper
- `templates/login.html` — wire up form action/method, remove redundant local error block

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On successful login, store `session["user_id"]` (and optionally `session["user_name"]`) — do not store the password hash in the session
- On failed login (unknown email or wrong password), flash a single generic error (e.g. "Invalid email or password") — do not reveal whether the email exists, and re-render the form without redirecting
- `GET /logout` must clear the session (`session.clear()`) and redirect to `url_for('login')`, with a flashed confirmation message (e.g. "You have been signed out")
- Use `abort(405)` if an unsupported HTTP method reaches `/login`
- Use `url_for()` for every internal link — never hardcode URLs
- Do not implement any session-protection/`login_required` decorator or guard other routes — that belongs to Step 4 (`/profile`) unless explicitly requested here

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting valid credentials (e.g. demo@spendly.com / demo123 from the seed data) logs in and redirects to `/profile`
- [ ] Submitting an unknown email re-renders the login form with a generic "Invalid email or password" error, no session set
- [ ] Submitting a known email with the wrong password re-renders the login form with the same generic error, no session set
- [ ] After logging in, `session["user_id"]` is set and matches the logged-in user's id
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login` with a confirmation flash message
- [ ] Visiting `/logout` while not logged in does not error — redirects to `/login` cleanly
