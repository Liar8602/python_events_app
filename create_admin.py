import sys
from getpass import getpass
from app import create_app
from app.user.models import User
from app.models import db

app = create_app()

with app.app_context():
    username = input('Enter the username: ')
    if User.query.filter(User.username == username).count():
        print('User with this name already exists')
        sys.exit(0)

    password1 = getpass('Get password: ')
    password2 = getpass('Repeat the password: ')
    if password1 != password2:
        print("Passwords don't match")
        sys.exit(0)
    new_user = User(username=username, role='admin')
    new_user.set_password(password1)
    db.session.add(new_user)
    db.session.commit()
    print(f'User with id={new_user.id} added')
