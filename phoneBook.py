import csv
from datetime import datetime
from contact import Contact

class PhoneBook:
    def __init__(self):
        self.contacts = []

    def add(self, contact):
        self.contacts.append(contact)

    def search_by_name(self, query):
        """Search contacts by name with wildcard support."""
        results = []
        for contact in self.contacts:
            if query.lower() in contact.first_name.lower() or query.lower() in contact.last_name.lower():
                results.append(contact)
        return results

    def search_by_phone(self, query):
        """Search contacts by phone with wildcard support."""
        results = []
        for contact in self.contacts:
            if query in contact.phone:
                results.append(contact)
        return results

    def search_by_timeframe(self, start_date=None, end_date=None):
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
        self.contacts = [c for c in self.contacts if c.phone != phone]

    def update(self, phone, first_name=None, last_name=None, email=None, address=None):
        for contact in self.contacts:
            if contact.phone == phone:
                contact.update(first_name, last_name, phone, email, address)

    def sort(self, by='last_name'):
        return sorted(self.contacts, key=lambda x: getattr(x, by))

    @staticmethod
    def log(operation, contact):
        with open('phonebook.log', 'a') as log_file:
            log_file.write(f'{operation} performed on {contact.first_name} {contact.last_name}\n')

    @staticmethod
    def get_history():
        with open('phonebook.log', 'r') as log_file:
            return log_file.readlines()
