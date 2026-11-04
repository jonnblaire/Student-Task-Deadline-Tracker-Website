## ⚙️ How the System Works (System Flow)

TaskFlow follows the standard **MVT (Model-View-Template)** architecture of Django. Here is the step-by-step flow of how data moves through the system:

### 1. User Interaction (Frontend)
- The user interacts with the UI (Templates) built with HTML, CSS, and JavaScript.
- For example, when a user clicks "Add New Task" and submits the form, a **POST request** is sent to the Django server.

### 2. URL Routing (`urls.py`)
- The request is intercepted by Django's URL dispatcher (`urls.py`). 
- It looks at the URL path (e.g., `/add-task/`) and routes it to the corresponding Python function in `views.py`.

### 3. View Processing (`views.py`)
- The **View** acts as the "brain" of the application. It receives the request, checks if it's a POST or GET request, and handles the logic.
- If a form is submitted, the view validates the data using Django **Forms** (`forms.py`).
- The view then communicates with the **Model** to save or fetch data.

### 4. Database & Models (`models.py`)
- **Models** represent the database tables. TaskFlow uses SQLite3 by default.
- When the view says "Save this task," Django translates that into an SQL `INSERT` query to store the data in the `db.sqlite3` file.
- When data is needed (e.g., loading the Dashboard), the model fetches the records.

### 5. Rendering the Response (Templates)
- After getting the data, the View packages it into a **Context** (a dictionary of data).
- It passes this context to the **Template** (HTML). Django then renders the HTML dynamically (e.g., looping through tasks with `{% for task in tasks %}`).
- Finally, the fully rendered HTML page is sent back to the user's browser.

### 🔄 Example: Adding a Task
1. **User** fills out the form in `add-task.html` and clicks "Save".
2. **URL** routes `/add-task/` to `views.add_task`.
3. **View** checks if the form is valid using `TaskForm`.
4. **Model** saves the new task to the SQLite database.
5. **View** redirects the user back to `/my-tasks/` with a success message.
6. **Template** renders the updated task list.
