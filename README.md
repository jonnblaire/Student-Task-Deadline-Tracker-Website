## 🔄 Detailed System Flow (Behind the Scenes)

TaskFlow follows the standard **Django MVT (Model-View-Template)** architecture. Here is the step-by-step flow of how data moves through the system when a user interacts with it:

### 1. Routing (`urls.py`)
- When a user clicks a button or types a URL (e.g., `/add-task/`), the request hits the `urls.py` file.
- Django acts like a traffic enforcer: it looks at the URL and routes the request to the correct Python function (View) in `views.py`.

### 2. The View (`views.py`)
- The **View** is the brain of the system. It receives the request and checks if it's a `GET` (loading a page) or a `POST` (submitting a form).
- If the user is submitting a form, the View validates the data using `forms.py`.
- The View then talks to the **Model** to fetch or save data.

### 3. The Model (`models.py`)
- The **Model** represents the Database (SQLite3).
- If the user adds a task, the View tells the Model to save it. The Model translates this into an SQL `INSERT` query.
- If the user views the Dashboard, the Model fetches all tasks and calculates the stats.

### 4. The Template (HTML)
- Once the View has the data (e.g., all tasks), it packages them into a "Context" (a dictionary).
- It sends this context to the **Template**.
- The Template uses Django tags (like `{% for task in tasks %}`) to dynamically render the HTML. 
- Finally, the browser receives the HTML and CSS, showing the updated page to the user.

---
### 📊 Example Scenario: Adding a Task
1. **User** fills out the "Add Task" form and clicks Submit.
2. **Browser** sends a `POST` request to the URL `/add-task/`.
3. **`urls.py`** routes the request to `views.add_task`.
4. **`views.py`** validates the form data via `forms.py`.
5. **`models.py`** saves the new task to the SQLite Database.
6. **`views.py`** redirects the user back to `/my-tasks/` and triggers a success message.
7. **Template** reloads and displays the newly added task in the table.
