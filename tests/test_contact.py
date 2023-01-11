import pytest
import contact


def test_invalid_init() -> None:
    with pytest.raises(ValueError) as excinfo:
        a = contact.Contact()
    assert "initialization parameters" in str(excinfo.value)


def test_with_first_name() -> None:
    a = contact.Contact("kevin")
    assert a.first_name == "kevin"
    assert not a.last_name
    assert len(a.email) == 0


def test_with_last_name() -> None:
    a = contact.Contact(last_name="goldsmith")
    assert a.last_name == "goldsmith"
    assert not a.first_name
    assert len(a.email) == 0


def test_with_email() -> None:
    a = contact.Contact(email="kevin@devnull.com")
    assert a.first_name == "kevin"
    assert not a.last_name
    assert a.email[0] == "kevin@devnull.com"

    b = contact.Contact(email="kevin.goldsmith@devnull.com")
    assert b.first_name == "kevin"
    assert b.last_name == "goldsmith"
    assert b.email[0] == "kevin.goldsmith@devnull.com"


def test_with_all() -> None:
    a = contact.Contact("kevin", "goldsmith", "foo@devnull.com")
    assert a.first_name == "kevin"
    assert a.last_name == "goldsmith"
    assert a.email[0] == "foo@devnull.com"
