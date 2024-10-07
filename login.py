from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
import bcrypt

# Running on http://127.0.0.1:5000

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong secret key

# PostgreSQL connection details (replace these with your actual DB details)
def get_db_connection():
    return psycopg2.connect(
        dbname="GreenLog",
        user="postgres",
        password="XzyxOCph4c",  # Replace with your actual password
        host="localhost",
        port="5432"
    )

# Login route to render the login form
@app.route('/')
def index():
    return render_template('login.html')  # Render the HTML login page

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password'].encode('utf-8')  # Convert password to bytes for bcrypt

    try:
        # Connect to the PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT paswoord FROM people_greenlog WHERE e_mail = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[0].encode('utf-8')):  # Check hashed password
            session['email'] = email  # Store email in the session for user authentication
            return redirect(url_for('dashboard'))  # Redirect to a dashboard or home page
        else:
            return 'Invalid email or password.', 401  # Return an error message on invalid credentials

    except psycopg2.Error as e:
        return f"Database error: {e}", 500  # Handle database connection errors

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Dashboard route (for successful login)
@app.route('/dashboard')
def dashboard():
    if 'email' in session:  # Check if the user is logged in
        return f"Welcome {session['email']}! You are logged in."
    else:
        return redirect(url_for('index'))  # If not logged in, redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)
