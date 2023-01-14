"""
    a list of contacts
"""
from typing import List

from contact import Contact


class ContactList:
    """
    a list of contacts that supports finding, and matching
    """

    def __init__(self) -> None:
        """
        __init__ initialize the object, set contacts to an empty list
        """
        self.contacts: List[Contact] = []

    def __str__(self) -> str:
        """
        __str__ return a string summary of the object

        Returns:
            str: a description of the object
        """
        return f"contact list: {len(self.contacts)} items"

    def add(self, new_contact: Contact) -> None:
        """
        add add a contact to the list, if the contact is already in the list, merge it

        Args:
            new_contact (Contact): the contact object to add
        """
        if new_contact in self.contacts:
            index = self.contacts.index(new_contact)
            self.contacts[index].merge(new_contact)
        else:
            self.contacts.append(new_contact)
