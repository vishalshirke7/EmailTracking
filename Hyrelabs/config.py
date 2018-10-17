DEBUG = False
TESTING = False
SECRET_KEY = b'\xa9||/\x9dp\x1b\x9f'
CLIENT_ID = ('1010563798082-2gon9gcgq7hegims91cn79ip64akbgcq''.apps.googleusercontent.com')
CLIENT_SECRET = 'ehnUQ5lVVxjQiXjKLB6YJTLl'
REDIRECT_URI = 'http://localhost:5000/gCallback'
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
SCOPE = ['profile', 'email', 'https://mail.google.com/']

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/hyrelabs_db'
