from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import bcrypt
import os
from urllib.parse import urlparse

#Running on http://127.0.0.1:5000

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Update this with a secure secret key

def get_db_connection():
    # Check if DATABASE_URL is set (used in production)
    database_url = os.environ.get("postgres://u84dqaci1j7g53:p5c8b92db5ffb0b519f9ea9f1c5e4caaa0aa5263f10fe45dba24d16d1de9c14b7@cfls9h51f4i86c.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dbn6bk22lafkc2")
    
    if database_url:
        result = urlparse(database_url)
        return psycopg2.connect(
            dbname=result.path[1:],  # Remove leading '/' to get the database name
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
    else:
        # Fallback to local development database
        return psycopg2.connect(
            dbname="GreenLog",
            user="postgres",
            password="XzyxOCph4c", 
            host="localhost",
            port="5432"
        )

#Databselink in GoogleDrive
#https://drive.google.com/file/d/1JjLec4J6ynPwOWKlILK-CAHR7mqehtnJ/view?usp=sharing
#Dowload link: https://drive.google.com/uc?export=download&id=1JjLec4J6ynPwOWKlILK-CAHR7mqehtnJ


# pricing function
#def getPrices(userID):
#    prices = [price1,price2,price3]
#    price1=8
#    price2= getDynamicPrice(userID)
#    price3= 4
#    return prices

#def getDynamicPrice(userID):
#    #check neighbours
#    #calcute costs with neighbour
#    #turn into price for consumer
#    return price

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
        cursor.execute("SELECT paswoord FROM people_greenlog WHERE email = %s", (email,))
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
