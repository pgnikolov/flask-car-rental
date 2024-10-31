# 🚗 Car Rental with Flask

A simple car rental web application built with Flask, providing essential features for managing car rentals, clients, and bookings.

## Features

- **User Authentication**: Secure login and registration for users and admins, with email verification for new users.
- **Car Management**: 
  - Add, edit, and delete cars from the inventory.
  - Filter cars by type, fuel, and seating capacity for better user experience.
- **Rental Management**: 
  - Create, view, and manage bookings for clients.
  - View car availability and rental history.
- **Admin Dashboard**: 
  - Overview and control of all cars, clients, and rental operations.
  - Manage car details like brand, model, year, color, rental price, and status (available/rented).
  

## 🛠️ Built With

- **Flask** - Backend framework for routing and handling requests.
- **SQLAlchemy**: An ORM (Object-Relational Mapping) library for Python, providing a full power and flexibility of SQL without the need for writing raw SQL queries.
- **SQLite** - Lightweight, local database for storing data.
- **HTML/CSS** - Frontend design and layout.
- **Bootstrap** - Responsive UI components.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/pgnikolov/flask-car-rental.git
   cd flask-car-rental
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:** Create a .env file for sensitive information:
    ```bash
   EMAIL_USER=your_email@example.com
   EMAIL_PASS=your_password
    ```

5. **Database Setup:** Run initial migrations:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
6. **Run the Application:**
   ```bash
   python app.py
   ```

7. **Access the App:**
   Open your browser and go to `http://127.0.0.1:5000`.


## Folder Structure

- **app/**: Contains the main application files, including routes, models, and forms.
- **static/**: Static resources like CSS, JavaScript, and images.
- **templates/**: Database migrations for schema management using Flask-Migrate.


## Libraries and Methods Used

- **Flask-SQLAlchemy**: Simplifies SQLAlchemy integration with Flask, making it easy to work with databases.
- **Flask-Migrate**: Handles database migrations, allowing for version control of database schema changes.
- **Flask-WTF**: Integrates WTForms with Flask,
- **Flask-Login**: Manages user sessions and authentication, making it easy to handle user logins.
- **Flask-Mail:** Sends email confirmations and notifications.
- **Itsdangerous:** Generates secure tokens, used for email confirmation. 
- **Werkzeug.security:** Provides utilities like password hashing to securely store and check user passwords.



--- 

Let me know if you'd like any additional sections added!