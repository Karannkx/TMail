from flask import Flask, request, render_template, jsonify
import sqlite3
import random
import string
import datetime
import time
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# create a Flask app
app = Flask(__name__)

# create a function to generate a random email address
def generate_email_address():
    domain = 'tempmail.com'
    prefix = ''.join(random.choices(string.ascii_lowercase, k=10))
    email = prefix + '@' + domain
    return email

# create a function to generate a random OTP
def generate_otp():
    digits = string.digits
    otp = ''.join(random.choice(digits) for i in range(6))
    return otp

# create a function to handle email delivery and management
def handle_email():
    # connect to the database
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    
    # create a table to store emails
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (id INTEGER PRIMARY KEY, email TEXT, sender TEXT, subject TEXT, body TEXT, created_at TEXT)''')
    
    # receive incoming emails and store them in the database
    while True:
        # simulate receiving emails every 10 seconds
        time.sleep(10)
        
        # generate a list of all email addresses in the database
        c.execute('SELECT email FROM emails')
        emails = c.fetchall()
        
        for email in emails:
            # simulate receiving new emails for each email address
            sender = 'example@gmail.com'
            subject = 'Test email'
            body = 'This is a test email.'
            created_at = datetime.datetime.now()
            
            # insert the new email into the database
            c.execute('INSERT INTO emails (email, sender, subject, body, created_at) VALUES (?, ?, ?, ?, ?)',
                      (email[0], sender, subject, body, created_at))
            conn.commit()
            
            # simulate deleting old emails after 1 day
            c.execute('DELETE FROM emails WHERE created_at < datetime("now", "-1 day")')
            conn.commit()
    
    # close the database connection
    conn.close()

# create a route to display the temporary email address and allow users to view and read incoming emails
@app.route('/')
def index():
    # generate a random email address
    email = generate_email_address()
    
    # generate a random OTP and store it in the session
    otp = generate_otp()
    session['otp'] = otp
    
    # render the index.html template with the email address
    return render_template('index.html', email=email)

# create a route to verify the OTP and display incoming emails
@app.route('/verify', methods=['POST'])
def verify():
    # retrieve the email and OTP from the form data
    email = request.form.get('email')
    otp = request.form.get('otp')
    
    # retrieve the stored OTP from the session
    stored_otp = session.get('otp')
    
    if stored_otp == otp:
        # if the OTP is correct, remove it from the session and redirect to the inbox page
        session.pop('otp', None)
        return redirect('/inbox?email=' + email)
    else:
        # if the OTP is incorrect, render an error message
        error = 'Invalid OTP. Please try again.'
        return render_template('index.html', email=email, error=error)

# create a route to display the inbox for a given email address
@app.route('/inbox')
def inbox():
    # retrieve
