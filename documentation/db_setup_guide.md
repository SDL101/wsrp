WSRP — DB Migration & Recovery Playbook
A quick, repeatable checklist for cutting over to a new Postgres DB on Render and verifying the app end-to-end.

0) Prereqs
Access to the Render dashboard for wsrp (web service) and the Postgres instance.

Local terminal with psql (or use Render’s Shell).

Repo checked out with the SQL seed file: database/database_setup_postgres.sql.

1) Create the new DB (Render)
In Render, create a new Postgres instance.

Copy its external connection string (looks like
postgresql://USER:PASSWORD@HOST:PORT/DBNAME).

Keep the old DB running until cutover verification is complete.

2) Update the app’s env
Render → wsrp (web service) → Environment:

Set DATABASE_URL to the new connection string.

Confirm CORS_ORIGINS, FLASK_SECRET_KEY, JWT_SECRET_KEY are present.

Save env changes, then Manual Deploy → Restart service (or “Clear build cache & deploy” if you changed packages).

Sanity-check from Render Shell:

echo $DATABASE_URL
# Should print the new DB URL
3) Initialize schema + seed data
From your local terminal (or Render Shell), run:

psql "postgresql://USER:PASSWORD@HOST/DBNAME" \
  -f database/database_setup_postgres.sql
Expected output ends with several:

CREATE TABLE
INSERT 0 N
4) Verify data in the new DB
Quick checks:

-- list tables
\dt

-- sample data
SELECT * FROM users;
SELECT * FROM accounts;
You should see the seeded employees/customers and accounts.

5) Smoke test the API (hits the new DB)
From anywhere:

curl -s https://wsrp-02i3.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"user_name":"db2_sanity","password":"Passw0rd!","first_name":"DB2","last_name":"Check","email":"db2_sanity@example.com","user_type":"CUSTOMER"}'
Expected:

{"message":"User registered successfully","status_code":201}
Confirm it landed in the new DB:

SELECT user_name, email FROM users WHERE email='db2_sanity@example.com';
6) Smoke test the frontend
Visit the hosted site (e.g., https://wsrp.space or the Render URL).

Register/login, view accounts/transactions.

If anything fails, check Render → Logs for the wsrp service.

7) Rollback plan (if needed)
Revert DATABASE_URL to the old connection string.

Restart the wsrp service.

(Optional) migrate any newly created data from the new DB back to the old via SQL dump/restore.

8) Backups & hygiene
Enable/confirm automated backups on Render Postgres.

Keep seed files Postgres-flavored only (database_setup_postgres.sql).

Avoid MySQL syntax (backticks, CREATE DATABASE, USE, etc.).

9) Common gotchas
Mismatched driver URL: Use postgresql:// (not postgresql+psycopg2:// unless your ORM requires it).

Service not reloaded: After changing env vars, Restart service.

CORS: Ensure CORS_ORIGINS includes both bare and www domains.

Rate limiter warning: Flask-Limiter in-memory storage is fine for dev; consider Redis for production.

10) Optional: Local quick test (without frontend)

export DATABASE_URL="postgresql://USER:PASSWORD@HOST/DBNAME"
pip install -r server/requirements.txt
cd server && gunicorn server:app
# then curl the local or deployed URL
11) One-liner cutover (summary)

# 1) Update env var on Render (UI)
# 2) Restart service (UI)
# 3) Seed new DB:
psql "postgresql://USER:PASSWORD@HOST/DBNAME" -f database/database_setup_postgres.sql
# 4) API sanity:
curl -s https://<your-app>/api/auth/register -H "Content-Type: application/json" -d '{"user_name":"db2_sanity","password":"Passw0rd!","first_name":"DB2","last_name":"Check","email":"db2_sanity@example.com","user_type":"CUSTOMER"}'
# 5) Verify in psql: SELECT * FROM users WHERE email='db2_sanity@example.com';