import pytest
from pydantic import ValidationError

from tweakers.user import User


def test_user_id():
    user = User(id=1)
    assert user


def test_user_name():
    user = User(name="Femme")
    assert user


def test_user_no_id_and_no_name():
    with pytest.raises(ValidationError):
        User()
