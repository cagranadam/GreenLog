import bcrypt
import psycopg2
import os
import random
import string

# Function to generate a random password
def generate_password(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Function to hash passwords
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Generate hashed password
    return hashed.decode('utf-8')  # Decode the binary to a string to store in the DB

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "GreenLog"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD","XzyxOCph4c"),  # Environment variable for password
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    cursor = connection.cursor()

    # Fetch all the users from people_greenlog table
    cursor.execute("SELECT id, email FROM people_greenlog")
    users = cursor.fetchall()

    for user_id, email in users:
        # Generate a random password for the user
        plain_password = generate_password()
        
        # Hash the generated password
        hashed_password = hash_password(plain_password)

        # Update the table with the hashed password
        cursor.execute(
            "UPDATE people_greenlog SET paswoord = %s WHERE id = %s",
            (hashed_password, user_id)
        )

        # Optional: Print or store the plain password for reference (you can save them securely)
        print(f"Generated password for {email}: {plain_password}")

    # Commit the changes to the database
    connection.commit()

except Exception as error:
    print(f"Error occurred: {error}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()

print("All passwords have been created, hashed, and stored successfully.")
