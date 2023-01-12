"""
    Contact class for a person
"""

"""
outlook_csv_properties = [
    'First Name', 'Middle Name', 'Last Name', 'Title', 'Suffix', 'Initials', 'Web Page',
    'Gender', 'Birthday', 'Anniversary', 'Location', 'Language', 'Internet Free Busy',
    'Notes', 'E-mail Address', 'E-mail 2 Address', 'E-mail 3 Address', 'Primary Phone',
    'Home Phone', 'Home Phone 2', 'Mobile Phone', 'Pager', 'Home Fax', 'Home Address',
    'Home Street', 'Home Street 2', 'Home Street 3', 'Home Address PO Box', 'Home City',
    'Home State', 'Home Postal Code', 'Home Country', 'Spouse', 'Children', 'Manager\'s Name',
    'Assistant\'s Name', 'Referred By', 'Company Main Phone', 'Business Phone', 'Business Phone 2',
    'Business Fax', 'Assistant\'s Phone', 'Company', 'Job Title', 'Department', 'Office Location',
    'Organizational ID Number', 'Profession', 'Account', 'Business Address', 'Business Street',
    'Business Street 2', 'Business Street 3', 'Business Address PO Box', 'Business City',
    'Business State', 'Business Postal Code', 'Business Country', 'Other Phone', 'Other Fax',
    'Other Address', 'Other Street', 'Other Street 2', 'Other Street 3', 'Other Address PO Box',
    'Other City', 'Other State', 'Other Postal Code', 'Other Country', 'Callback', 'Car Phone',
    'ISDN', 'Radio Phone', 'TTY/TDD Phone', 'Telex', 'User 1', 'User 2', 'User 3', 'User 4',
    'Keywords', 'Mileage', 'Hobby', 'Billing Information', 'Directory Server', 'Sensitivity',
    'Priority', 'Private', 'Categories'
]
"""


class Contact:
    """
    class to represent a person
    """

    def __init__(
        self, first_name: str = "", last_name: str = "", email: str = ""
    ) -> None:
        """
        __init__ initialize a contact with names and an e-mail address. If only the
        email address is provided it is used to infer the first and last names

        Args:
            first_name (str, optional): first name. Defaults to ''.
            last_name (str, optional): last name. Defaults to ''.
            email (str, optional): e-mail address. Defaults to ''.

        Raises:
            ValueError: _description_
        """
        if len(first_name) + len(last_name) + len(email) == 0:
            raise ValueError("all initialization parameters are empty")
        if email:
            self.email = [email]
        else:
            self.email = []
        if email and (not first_name and not last_name):
            at_pos = email.find("@")
            name = email[:at_pos]
            period_pos = name.find(".")
            if period_pos > -1:
                self.first_name = name[:period_pos]
                self.last_name = name[period_pos + 1 :]
            else:
                self.first_name = name
                self.last_name = ""
        else:
            self.first_name = first_name
            self.last_name = last_name

    def __str__(self) -> str:
        """
        __str__ _summary_

        Returns:
            str: a string representation of the object
        """
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __eq__(self, __o: object) -> bool:
        """
        __eq__ overrides the default equality

        Args:
            __o (object): _description_

        Returns:
            bool: _description_
        """
        if not isinstance(__o, self.__class__):
            return False
        if (self.first_name == __o.first_name) and (self.last_name == __o.last_name):
            if len(list(set(self.email) & set(__o.email))) > 0:
                # at least one e-mail address in common
                return True
            return len(self.first_name) > 0 and len(self.last_name) > 0
        return False

    def merge(self, other: object) -> None:
        """
        merge _summary_

        Args:
            other (object): _description_

        Raises:
            ValueError: _description_
        """
        if not isinstance(other, self.__class__):
            raise ValueError(
                f"attempt to merge an instance of {other.__class__} into a Contact instance"
            )
        if not self.first_name and other.first_name:
            self.first_name = other.first_name
        if not self.last_name and other.last_name:
            self.last_name = other.last_name
        print(f"self.email {self.email} - other.email {other.email}")
        self.email.extend(other.email)
        if len(self.email) > 0:
            self.email = list(set(self.email))
