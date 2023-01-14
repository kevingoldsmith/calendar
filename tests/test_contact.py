import pytest
import contact


def test_invalid_init() -> None:
    with pytest.raises(ValueError) as excinfo:
        a = contact.Contact()
    assert "initialization parameters" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        a = contact.Contact(email=[])
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


def test_with_email_list() -> None:
    a = contact.Contact(email=["kevin@devnull.com"])
    assert a.first_name == "kevin"
    assert not a.last_name
    assert a.email[0] == "kevin@devnull.com"

    b = contact.Contact(email=["kevin@devnull.com", "kevin.goldsmith@devnull.com"])
    assert b.first_name == "kevin"
    assert b.last_name == "goldsmith"
    assert b.email[1] == "kevin.goldsmith@devnull.com"


def test_with_all() -> None:
    a = contact.Contact("kevin", "goldsmith", "foo@devnull.com")
    assert a.first_name == "kevin"
    assert a.last_name == "goldsmith"
    assert a.email[0] == "foo@devnull.com"


def test_equals() -> None:
    a = contact.Contact("kevin", "goldsmith", "foo@devnull.com")
    b = contact.Contact("kevin", "goldsmith", "foo@devnull.com")
    c = contact.Contact("kevin", "goldsmith")
    d = contact.Contact("kevin", "goldsmith", "pa@devnull.com")
    d.email.append("foo@devnull.com")
    g = contact.Contact("kevin", "goldsmith", "pa@devnull.com")

    assert a == b
    assert a == c
    assert a == d
    assert b == c
    assert b == d
    assert c == d
    assert a == g

    e = contact.Contact("kevin")
    assert a != e
    f = contact.Contact(last_name="goldsmith")
    assert a != f


def test_merge() -> None:
    a = contact.Contact("kevin")
    b = contact.Contact(last_name="goldsmith")
    c = contact.Contact(email="foo@devnull.com")
    d = contact.Contact(email="pa@devnull.com")

    with pytest.raises(ValueError) as excinfo:
        a.merge(dict)
    assert "attempt to merge an instance of" in str(excinfo.value)

    a.merge(b)
    a.merge(c)
    a.merge(d)
    e = contact.Contact("kevin", "goldsmith", "pa@devnull.com")
    e.email.append("foo@devnull.com")
    assert a == e


def test_to_dict() -> None:
    b = contact.Contact(email=["kevin@devnull.com", "kevin.goldsmith@devnull.com"])
    d = b.to_dict()
    assert d["first_name"] == "kevin"
    assert d["last_name"] == "goldsmith"
    assert d["email"][1] == "kevin.goldsmith@devnull.com"
