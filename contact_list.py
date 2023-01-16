"""
    a list of contacts
"""
from copy import deepcopy
import csv
import os
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

        Raises:
            KeyError: if the new_contact contains multiple e-mail addresses and they map to different contacts
        """
        if len(new_contact.email) > 1:
            contact_match = None
            for em in new_contact.email:
                c = self.find_by_email(em)
                if not contact_match:
                    contact_match = c
                elif c != contact_match:
                    raise KeyError("more than one contact mapping to the addresses in this contact")

        c = self.find_by_email(new_contact.email[0])
        if c:
            c.merge(new_contact)
        elif new_contact in self.contacts:
            index = self.contacts.index(new_contact)
            self.contacts[index].merge(new_contact)
        else:
            self.contacts.append(new_contact)

    def find_by_email(self, email: str) -> Contact|None:
        """
        find_by_email see if there is a contact for a given e-mail address, they should be unique

        Args:
            email (str): the e-mail to search for

        Returns:
            Contact|None: the Contact if there is one, otherwise None
        """
        for contact in self.contacts:
            if email in contact.email:
                return contact
        return None

    def load_from_file(self, filename: str = "contacts.csv") -> None:
        """
        load_from_file _summary_

        Args:
            filename (str, optional): _description_. Defaults to 'contacts.csv'.

        Raises:
            FileNotFoundError: if the file does not exist
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"file does not exist{filename}")
        with open(filename, "r", encoding="utf-8") as file:
            csvreader = csv.DictReader(file, dialect="excel")
            for row in csvreader:
                emails = []
                for key in row.keys():
                    if key.startswith("email") and len(row[key]) > 0:
                        emails.append(row[key])
                self.contacts.append(
                    Contact(row["first_name"], row["last_name"], emails)
                )

    def save_to_file(self, filename: str = "contacts.csv") -> None:
        """
        save_to_file save the contents of the list to a csv file

        Args:
            filename (str, optional): the file to save to. Defaults to 'contacts.csv'.
        """
        # find the highest number of e-mail addresses
        email_count = 0
        for contact_item in self.contacts:
            if len(contact_item.email) > email_count:
                email_count = len(contact_item.email)
        field_names = ["first_name", "last_name"]
        for i in range(0, email_count):
            field_names.append(f"email_{i+1}")
        with open(filename, "w", encoding="utf-8") as file:
            csvwriter = csv.DictWriter(file, fieldnames=field_names, dialect="excel")
            csvwriter.writeheader()
            for contact_item in self.contacts:
                row_dict = deepcopy(contact_item.to_dict())
                i = 1
                for email_addr in row_dict["email"]:
                    row_dict[f"email_{i}"] = email_addr
                    i = i + 1
                del row_dict["email"]
                csvwriter.writerow(row_dict)
