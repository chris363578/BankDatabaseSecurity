# Bank Database Security - Django Project

## Setup Instructions

1. **Install Required Packages**  
    Run the following command to install all required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. **Apply Migrations**  
    Apply database migrations to set up the database schema:
    ```bash
    python manage.py migrate
    ```

3. **Run the Development Server**  
    Start the Django development server:
    ```bash
    python manage.py runserver
    ```

4. **Access the Application**  
    Open your browser and navigate to:
    ```
    http://127.0.0.1:8000/
    ```

5. **Create a Superuser (Optional)**  
    To access the admin panel, create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. **Admin Panel**  
    Access the admin panel at:
    ```
    http://127.0.0.1:8000/admin/
    ```

## Notes
- Ensure you have Python and Django installed.
- Use a virtual environment to avoid dependency conflicts.
- Update the `settings.py` file as needed for your environment.
- For production, configure a proper database and static file hosting.
