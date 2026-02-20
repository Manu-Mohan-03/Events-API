#import pytest
from models import User

def test_user_password():
    user = User(username='John')
    user.password = user.set_password('init1234')

    #check if password is correct
    assert user.check_password('init1234') is True
    # check wrong password
    assert  user.check_password('John1234') is False
    # check password hashing
    assert user.password_hash != user.password

