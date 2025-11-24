# Sustainability Actions App

This project implements the assignment:

- A **Django REST API** backend for tracking sustainability actions.
- A **React** frontend that talks to the backend via **Axios**.
- API endpoints tested with **Postman**.

The backend stores actions in a JSON file and supports full CRUD (create, read, update, delete). The frontend provides a simple UI to list, add, edit, and delete actions.

---

## 1. Project Structure

At the top level:

- `backend/` – Django API (Python)
- `frontend/` – React app (JavaScript)

Run the backend and frontend in **separate terminals**.

---

## 2. Backend (Django API)

### 2.1 Requirements

- Python 3
- `pip` (Python package manager)

### 2.2 First-time setup

From the top-level folder (`sustainability-app`):

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework
python manage.py migrate
The code assumes there is a Django project called backend_project and an app called actions inside backend/.

2.3 Run the backend server
From inside the backend folder, with the virtual environment activated:

bash
Copy code
cd backend        # if you're not already inside the backend folder
source venv/bin/activate
python manage.py runserver
The backend will be available at:

text
Copy code
http://localhost:8000/
2.4 API endpoints
Base URL:

text
Copy code
http://localhost:8000/api/actions/
Endpoints:

GET /api/actions/ – list all actions

POST /api/actions/ – create a new action

GET /api/actions/<id>/ – get a single action (optional but implemented)

PUT /api/actions/<id>/ – replace an action

PATCH /api/actions/<id>/ – partially update an action

DELETE /api/actions/<id>/ – delete an action

Example POST payload:

json
Copy code
{
  "action": "Recycling",
  "date": "2025-01-08",
  "points": 25
}
2.5 Data storage
The API uses a JSON file located in the actions app:

backend/actions/actions.json

Each action has the following fields:

id (integer, primary key)

action (string, max length 255)

date (string in YYYY-MM-DD format)

points (integer)

3. Frontend (React app)
3.1 Requirements
Node.js

npm (comes with Node.js)

3.2 First-time setup
From the top-level folder (sustainability-app):

bash
Copy code
cd frontend
npm install
This installs React, Axios, and other dependencies listed in package.json.

The package.json includes a proxy:

json
Copy code
"proxy": "http://localhost:8000"
This allows the React app to call the Django API using relative URLs like /api/actions/ during development.

3.3 Run the frontend
From inside the frontend folder:

bash
Copy code
cd frontend
npm start
This starts the React development server at:

text
Copy code
http://localhost:3000/
With the backend running, you can:

Add a new action (Action Name, Date, Points) via the form.

See actions in a table (ID, Action, Date, Points).

Edit an existing action (sends a PUT request).

Delete an action (sends a DELETE request).

The table is refreshed after successful create/update/delete.

4. Testing the API with Postman
You can use Postman (or any HTTP client) to test the backend API directly.

4.1 List actions
Method: GET

URL: http://localhost:8000/api/actions/

Example response:

json
Copy code
[
  {
    "id": 1,
    "action": "Recycling",
    "date": "2025-01-08",
    "points": 25
  }
]
4.2 Create an action
Method: POST

URL: http://localhost:8000/api/actions/

Body (JSON):

json
Copy code
{
  "action": "Recycling",
  "date": "2025-01-08",
  "points": 25
}
4.3 Update an action
Method: PUT

URL: http://localhost:8000/api/actions/1/

Body (JSON):

json
Copy code
{
  "action": "Carpooling",
  "date": "2025-01-09",
  "points": 15
}
4.4 Delete an action
Method: DELETE

URL: http://localhost:8000/api/actions/1/

Returns HTTP 204 No Content on success.
