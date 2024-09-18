from datetime import datetime

class Contact:
    """
    A class to represent a contact entry in the phone book.

    Attributes:
    -----------
    first_name : str
        The first name of the contact.
    last_name : str
        The last name of the contact.
    phone : str
        The phone number of the contact.
    email : str, optional
        The email address of the contact (default is None).
    address : str, optional
        The address of the contact (default is None).
    time_added : datetime
        The timestamp when the contact was created.
    """

    def __init__(self, first_name, last_name, phone, email=None, address=None):
        """
        Initializes a new Contact object with the provided information.

        Parameters:
        -----------
        first_name : str
            The first name of the contact.
        last_name : str
            The last name of the contact.
        phone : str
            The phone number of the contact.
        email : str, optional
            The email address of the contact (default is None).
        address : str, optional
            The address of the contact (default is None).
        """
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.time_added = datetime.now()  # Store the timestamp when the contact is created

    def update(self, first_name=None, last_name=None, phone=None, email=None, address=None):
        """
        Updates the contact's information with the new values provided.

        Any parameter can be omitted, and if omitted, the current value will be retained.

        Parameters:
        -----------
        first_name : str, optional
            The new first name of the contact (default is None).
        last_name : str, optional
            The new last name of the contact (default is None).
        phone : str, optional
            The new phone number of the contact (default is None).
        email : str, optional
            The new email address of the contact (default is None).
        address : str, optional
            The new address of the contact (default is None).
        """
        if first_name:
            self.first_name = first_name  # Update the first name if provided
        if last_name:
            self.last_name = last_name  # Update the last name if provided
        if phone:
            self.phone = phone  # Update the phone number if provided
        if email:
            self.email = email  # Update the email if provided
        if address:
            self.address = address  # Update the address if provided

