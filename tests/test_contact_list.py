import pytest
import contact
import contact_list


def test_init() -> None:
    list = contact_list.ContactList()
    assert len(list.contacts) == 0


def test_str() -> None:
    list = contact_list.ContactList()
    assert str(list) == "contact list: 0 items"

    a = contact.Contact("kevin", "goldsmith", "foo@devnull.com")
    b = contact.Contact("fred", "flintstone", "ff@aol.com")
    c = contact.Contact("Barney", "Rubble", "br@foobar.org")
    list.add(a)
    list.contacts.append(b)
    list.add(c)
    assert str(list) == "contact list: 3 items"


def test_add() -> None:
    list = contact_list.ContactList()
    assert len(list.contacts) == 0

    list.add(contact.Contact("kevin", "goldsmith", "foo@devnull.com"))
    list.add(contact.Contact("fred", "flintstone", "ff@aol.com"))
    list.add(contact.Contact("Barney", "Rubble", "br@foobar.org"))
    assert len(list.contacts) == 3

    list.add(contact.Contact("kevin", "goldsmith", "blah@devnull.com"))
    assert len(list.contacts) == 3

    found_kevin = False
    for contact_item in list.contacts:
        if contact_item.first_name == "kevin":
            assert len(contact_item.email) == 2
            found_kevin = True
            break
        assert found_kevin
