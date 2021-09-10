from datetime import timedelta
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, '..', 'app.db')
SQLALCHEMY_TRACK_MODIFICATION = False

SECRET_KEY = '254b15d06fcaa941ed90eb23050ce02d28f769ef08ec12ead29086c9b54de66e'

REMEMBER_COOKIE_DURATION = timedelta(days=7)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "Your email"
MAIL_PASSWORD = 'Password for email'
DB_PATH = r"C:\projects\final\flask_events_app\flask_events_app\webapp/db"
