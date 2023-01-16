import os
import pytest

import pathlib

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

def test_add_invalid() -> None:
    list = contact_list.ContactList()
    list.add(contact.Contact("kevin", "goldsmith", "foo@devnull.com"))
    list.add(contact.Contact("fred", "flintstone", "ff@aol.com"))
    list.add(contact.Contact("Barney", "Rubble", ["br@foobar.org", "wqeqw@qweqw.qweq"]))
    with pytest.raises(KeyError) as excinfo:
        list.add(contact.Contact("toby", "mcquire", ["br@foobar.org", "ff@aol.com"]))
    assert "more than one contact mapping to the addresses in this contact" in str(excinfo.value)


def test_find_by_email() -> None:
    list = contact_list.ContactList()
    list.add(contact.Contact("kevin", "goldsmith", ["foo@devnull.com", "blah@devnull.com"]))
    list.add(contact.Contact("fred", "flintstone", "ff@aol.com"))
    list.add(contact.Contact("Barney", "Rubble", "br@foobar.org"))
    assert not list.find_by_email('qweqweqwe')
    assert list.find_by_email("br@foobar.org") == contact.Contact("Barney", "Rubble", "br@foobar.org")
    assert list.find_by_email("blah@devnull.com") == contact.Contact("kevin", "goldsmith", ["foo@devnull.com", "blah@devnull.com"])


def test_save_to_file(tmp_path: pathlib.Path) -> None:
    list = contact_list.ContactList()
    list.add(contact.Contact("kevin", "goldsmith", "foo@devnull.com"))
    list.add(contact.Contact("fred", "flintstone", "ff@aol.com"))
    list.add(contact.Contact("Barney", "Rubble", "br@foobar.org"))
    test_file_name = str(tmp_path / "testfile.csv")
    list.save_to_file(test_file_name)

    assert os.path.exists(test_file_name)


def test_load_from_file(tmp_path: pathlib.Path) -> None:
    list = contact_list.ContactList()
    list.add(contact.Contact("kevin", "goldsmith", "foo@devnull.com"))
    list.add(contact.Contact("fred", "flintstone", "ff@aol.com"))
    list.add(contact.Contact("Barney", "Rubble", ["br@foobar.org", "wqeqw@qweqw.qweq"]))
    test_file_name = str(tmp_path / "testfile.csv")
    list.save_to_file(test_file_name)

    list2 = contact_list.ContactList()
    list2.load_from_file(test_file_name)
    assert len(list2.contacts) == 3
    assert list2.contacts[2] == list.contacts[2]
