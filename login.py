from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Update this with a secure secret key

# PostgreSQL connection details
def get_db_connection():
    return psycopg2.connect(
        dbname="GreenLog",
        user="postgres",
        password="XzyxOCph4c",  # Use the correct database password
        host="localhost",
        port="5432"
    )

# Login route to render login form
@app.route('/')
def index():
    return render_template('login.html')  # This renders the login.html file

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password'].encode('utf-8')

    try:
        # Connect to the PostgreSQL database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT paswoord FROM people_greenlog WHERE e_mail = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user[0].encode('utf-8')):  # Check hashed password
            session['email'] = email  # Store email in session
            return redirect(url_for('afterlogin', email=email))  # Redirect to personal information page
        else:
            return 'Invalid email or password', 401

    except psycopg2.Error as e:
        return f"Database error: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

# Personal Information route (after successful login)
@app.route('/afterlogin')
def afterlogin():
    if 'email' in session:  # Check if the user is logged in
        email = request.args.get('email')  # Get email from query parameters
        return render_template('afterlogin.html', email=email)  # Render personal information page
    else:
        return redirect(url_for('index'))  # If not logged in, redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)
