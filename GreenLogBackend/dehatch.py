import bcrypt

# Replace 'your_password_here' with the password you want to test
plain_password = '$2b$12$lDAX8dbiqkYIU5Fm/e.j.uvDjgwqnCU9UKCBW2URNAYRKC5gj7qqy'
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

print(hashed_password.decode('utf-8'))
