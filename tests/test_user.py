from tweakers.user import User


def test_user_id():
    user = User(id=1)
    assert user


def test_user_name():
    user = User(name="Femme")
    assert user
