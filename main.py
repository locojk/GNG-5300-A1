import sys
import re
import pandas as pd

from phoneBook import PhoneBook
from contact import Contact

def display_menu():
    print("Phone Book Application, please select an option by type the related number:")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. View Audit History")
    print("7. Quit")

def validate_phone(phone):
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    return re.match(pattern, phone) is not None

def input_phone_number():
    phone = input("Phone number: ")
    return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def add_contact(phone_book):
    print("Please chose the add method")
    print("1. Add contact individually")
    print("2. Add contact from CSV file")

    input_choice = input("Enter your choice: ")
    if input_choice == "1":
        add_contact(phone_book)
    elif input_choice == "2":
        import_contacts(phone_book)
    else:
        print("Invalid choice, please try again.")

    if input_choice == "1":
        first_name = input("First Name: ")
        last_name = input("Last Name: ")

        phone = input_phone_number()

        while not validate_phone(phone):
            print("Invalid phone number format. Please enter in the format (###) ###-####.")
            phone = input_phone_number()

        email = input("Email (Optional): ")

        while email and not validate_email(email):
            print("Invalid email format. Please enter a valid email address.")
            email = input("Email (Optional): ")

        address = input("Address (Optional): ")

        contact = Contact(first_name, last_name, phone, email, address)
        phone_book.add(contact)

        phone_book.log("Add", contact)
        print(f"Added contact {first_name} {last_name}.")

    elif input_choice == "2":

        csv_file = input("Enter the path to the CSV file: ")

        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Iterate through the DataFrame rows
            for index, row in df.iterrows():
                # Ensure required columns are present
                if 'First Name' in df.columns and 'Last Name' in df.columns and 'Phone' in df.columns:
                    contact = Contact(row['First Name'], row['Last Name'], row['Phone'], row.get('Email', None),
                                      row.get('Address', None))
                    phone_book.add(contact)
                    phone_book.log("Add", contact)
                    print(f"Added contact {row['First Name']} {row['Last Name']}.")
                else:
                    print(f"Skipping, missing required fields")

        except FileNotFoundError:
            print(f"File {csv_file} not found.")
        except pd.errors.EmptyDataError:
            print("The CSV file is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        print("Invalid choice, please try again.")

def view_contacts(phone_book):
    contacts = phone_book.sort()
    for contact in contacts:
        print(f"{contact.first_name} {contact.last_name}, Phone: {contact.phone}, Email: {contact.email}")

def search_contacts(phone_book):
    print("Please chose the search method")
    print("1. Search by name")
    print("2. Search by phone number")
    print("3. Search by date range")

    input_choice = input("Enter your choice: ")
    if input_choice == "1":
        query = input("Enter the name to search: ")
        results = phone_book.search_by_name(query)
    elif input_choice == "2":
        query = input("Enter the phone number to search: ")
        results = phone_book.search_by_phone(query)
    elif input_choice == "3":
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        results = phone_book.search_by_timeframe(start_date, end_date)
    else:
        print("Invalid choice, please try again.")
        return

    for contact in results:
        print(f"{contact.first_name} {contact.last_name}, Phone: {contact.phone}")

def update_contact(phone_book):
    phone = input("Enter phone number of the contact to update: ")
    first_name = input("New First Name (or leave blank to keep current): ")
    last_name = input("New Last Name (or leave blank to keep current): ")
    email = input("New Email (or leave blank to keep current): ")
    address = input("New Address (or leave blank to keep current): ")
    phone_book.update(phone, first_name, last_name, email, address)
    print(f"Contact with phone number {phone} updated.")

def delete_contact(phone_book):
    phone = input("Enter phone number of the contact to delete: ")
    phone_book.delete(phone)
    print(f"Deleted contact with phone number {phone}.")

def import_contacts(phone_book):
    csv_file = input("Enter the path to the CSV file: ")
    phone_book.add_from_csv(csv_file)
    print("Contacts imported successfully.")

def view_audit_history(phone_book):
    history = phone_book.get_history()
    for log in history:
        print(log)

def main():
    phone_book = PhoneBook()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact(phone_book)
        elif choice == "2":
            view_contacts(phone_book)
        elif choice == "3":
            search_contacts(phone_book)
        elif choice == "4":
            update_contact(phone_book)
        elif choice == "5":
            delete_contact(phone_book)
        elif choice == "6":
            view_audit_history(phone_book)
        elif choice == "7":
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

