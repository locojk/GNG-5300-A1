from datetime import datetime
from contact import Contact

class PhoneBook:
    """
    A class to represent a phone book that manages a collection of contacts.

    The PhoneBook class provides methods to add, search, update, delete, sort, and group contacts.
    It also supports logging operations with timestamps, and can retrieve a log history.

    Attributes:
    -----------
    contacts : list
        A list to store Contact objects.

    Methods:
    --------
    add(contact):
        Adds a new contact to the phone book.

    search_by_name(query):
        Searches for contacts by first or last name using a case-insensitive wildcard search.

    search_by_phone(query):
        Searches for contacts by phone number using a wildcard search.

    search_by_timeframe(start_date=None, end_date=None):
        Searches for contacts added within a specified time frame.

    delete(phone):
        Deletes a contact by phone number.

    update(phone, first_name=None, last_name=None, email=None, address=None):
        Updates a contact's information by phone number.

    sort(by='last_name'):
        Sorts the contacts based on the specified attribute (default is last name).

    group_by(by='last_name'):
        Groups contacts by the specified attribute (default is last name).

    log(operation, contact=None):
        Logs the operation performed with an optional contact and timestamp.

    get_history():
        Retrieves the log history of operations performed.
    """

    def __init__(self):
        """Initializes an empty list to store contacts."""
        self.contacts = []

    def add(self, contact):
        """Adds a new contact to the phone book."""
        self.contacts.append(contact)

    def search_by_name(self, query):
        """
        Searches contacts by first or last name using case-insensitive wildcard matching.

        Parameters:
        -----------
        query : str
            The name query to search for in the contact list.

        Returns:
        --------
        results : list
            A list of contacts that match the query.
        """
        results = []
        for contact in self.contacts:
            if query.lower() in contact.first_name.lower() or query.lower() in contact.last_name.lower():
                results.append(contact)
        return results

    def search_by_phone(self, query):
        """
        Searches contacts by phone number using wildcard matching.

        Parameters:
        -----------
        query : str
            The phone number (or part of it) to search for in the contact list.

        Returns:
        --------
        results : list
            A list of contacts that match the phone number.
        """
        results = []
        for contact in self.contacts:
            if query in contact.phone:
                results.append(contact)
        return results

    def search_by_timeframe(self, start_date=None, end_date=None):
        """
        Searches for contacts added within a specified time frame.

        Parameters:
        -----------
        start_date : str, optional
            The start date in YYYY-MM-DD format.
        end_date : str, optional
            The end date in YYYY-MM-DD format.

        Returns:
        --------
        results : list
            A list of contacts added within the specified date range.
        """
        results = []

        # Parse and validate date range if provided
        def parse_date(date_string):
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                print(f"Invalid date format: {date_string}. Use YYYY-MM-DD format.")
                return None

        start_date_parsed = parse_date(start_date) if start_date else None
        end_date_parsed = parse_date(end_date) if end_date else None

        for contact in self.contacts:
            # Filter by date range if provided
            if start_date_parsed and contact.time_added < start_date_parsed:
                continue
            if end_date_parsed and contact.time_added > end_date_parsed:
                continue

            # If contact falls within the time range, add to results
            results.append(contact)

        return results

    def delete(self, phone):
        """
        Deletes a contact by phone number.

        Parameters:
        -----------
        phone : str
            The phone number of the contact to be deleted.
        """
        self.contacts = [c for c in self.contacts if c.phone != phone]

    def update(self, phone, first_name=None, last_name=None, email=None, address=None):
        """
        Updates a contact's information by phone number.

        Parameters:
        -----------
        phone : str
            The phone number of the contact to update.
        first_name : str, optional
            The new first name of the contact.
        last_name : str, optional
            The new last name of the contact.
        email : str, optional
            The new email of the contact.
        address : str, optional
            The new address of the contact.
        """
        for contact in self.contacts:
            if contact.phone == phone:
                contact.update(first_name, last_name, phone, email, address)

    def sort(self, by='last_name'):
        """
        Sorts the contacts by the specified attribute.

        Parameters:
        -----------
        by : str
            The attribute to sort the contacts by (default is 'last_name').

        Returns:
        --------
        list
            The sorted list of contacts.
        """
        return sorted(self.contacts, key=lambda x: getattr(x, by))

    def group_by(self, by='last_name'):
        """
        Groups contacts by the specified attribute.

        Parameters:
        -----------
        by : str
            The attribute to group the contacts by (default is 'last_name').

        Returns:
        --------
        dict
            A dictionary where keys are the group value and values are lists of contacts.
        """
        groups = {}
        for contact in self.contacts:
            key = getattr(contact, by)
            if key not in groups:
                groups[key] = []
            groups[key].append(contact)
        return groups

    @staticmethod
    def log(operation, contact=None):
        """
        Logs operations with an optional contact and timestamp.

        Parameters:
        -----------
        operation : str
            The operation being logged (e.g., 'Add', 'Update', 'Delete').
        contact : Contact, optional
            The contact the operation was performed on (default is None).
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open('phonebook.log', 'a') as log_file:
            if contact is None:
                log_file.write(f'[{timestamp}] {operation} performed\n')
            else:
                log_file.write(f'[{timestamp}] {operation} performed on {contact.first_name} {contact.last_name}\n')

    @staticmethod
    def get_history():
        """
        Retrieves the log history of operations performed on the phone book.

        Returns:
        --------
        list
            A list of log entries.
        """
        with open('phonebook.log', 'r') as log_file:
            return log_file.readlines()

