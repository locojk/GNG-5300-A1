from datetime import datetime

class Contact:
    def __init__(self, first_name, last_name, phone, email=None, address=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address
        self.time_added = datetime.now()

    def update(self, first_name=None, last_name=None, phone=None, email=None, address=None):
        if first_name: self.first_name = first_name
        if last_name: self.last_name = last_name
        if phone: self.phone = phone
        if email: self.email = email
        if address: self.address = address
