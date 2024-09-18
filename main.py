import sys
# Regular expression library for validating
import re
# Pandas library for reading CSV files
import pandas as pd

from phoneBook import PhoneBook
from contact import Contact


def display_menu():
    """
    Displays the main menu with options for the user to select an action.
    """
    print("\nPhone Book Application, please select an option by typing the related number:")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contacts")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. View Audit History")
    print("7. Quit")


def validate_phone(phone):
    """
    Validates a phone number based on the pattern (###) ###-####.

    Parameters:
    -----------
    phone : str
        The phone number to be validated.

    Returns:
    --------
    bool
        True if the phone number matches the pattern, False otherwise.
    """
    pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    return re.match(pattern, phone) is not None


def input_phone_number():
    """
    Takes raw phone number input and formats it as (###) ###-####.

    Returns:
    --------
    str
        The formatted phone number.
    """
    phone = input("Phone number: ")
    return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"


def validate_email(email):
    """
    Validates an email address using a basic regex pattern.

    Parameters:
    -----------
    email : str
        The email to be validated.

    Returns:
    --------
    bool
        True if the email matches the pattern, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def add_contact(phone_book):
    """
    Adds a new contact either individually or by importing from a CSV file.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book where the contact will be added.
    """
    while True:
        print("Please choose the add method")
        print("1. Add contact individually")
        print("2. Add contact from CSV file")

        input_choice = input("Enter your choice: ")

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

            break

        elif input_choice == "2":
            csv_file = input("Enter the path to the CSV file: ")

            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file)

                if 'First Name' in df.columns and 'Last Name' in df.columns and 'Phone' in df.columns:
                    # Iterate through the DataFrame rows
                    for index, row in df.iterrows():
                        # Validate phone number
                        phone = row['Phone']
                        if not validate_phone(phone):
                            print(f"Invalid phone number format in row.")
                            return  # Stop further processing

                        # Validate email if provided
                        email = row.get('Email', None)
                        if email and not validate_email(email):
                            print(f"Invalid email format in row.")
                            return  # Stop further processing

                        # Create the contact and add it to the phone book
                        contact = Contact(row['First Name'], row['Last Name'], phone, email, row.get('Address', None))
                        phone_book.add(contact)
                        phone_book.log("Add", contact)
                        print(f"Added contact {row['First Name']} {row['Last Name']}.")

                break

            except FileNotFoundError:
                print(f"File {csv_file} not found.")
            except pd.errors.EmptyDataError:
                print("The CSV file is empty.")
            except Exception as e:
                print(f"An error occurred: {e}")

        else:
            print("\nInvalid choice, please try again.\n")


def view_contacts(phone_book):
    """
    Displays all contacts in the phone book, sorted alphabetically by last name.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book containing the contacts to display.
    """
    contacts = phone_book.sort()

    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        print(f"{contact.first_name} {contact.last_name} \nPhone: {contact.phone} \nEmail: {contact.email}\n")

    phone_book.log("View")


def search_contacts(phone_book):
    """
    Allows searching for contacts by name, phone number, or date range.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book to search in.
    """
    while True:
        print("Please choose the search method")
        print("1. Search by name")
        print("2. Search by phone number")
        print("3. Search by date range")

        input_choice = input("Enter your choice: ")

        if input_choice == "1":
            query = input("Enter the name to search: ")
            results = phone_book.search_by_name(query)
            if not results:
                print("No contacts found.")
            for contact in results:
                print(f"{contact.first_name} {contact.last_name}, Phone: {contact.phone}")
                phone_book.log("Search", contact)
            break
        elif input_choice == "2":
            query = input_phone_number()
            results = phone_book.search_by_phone(query)
            if not results:
                print("No contacts found.")
            for contact in results:
                print(f"{contact.first_name} {contact.last_name}, Phone: {contact.phone}")
                phone_book.log("Search", contact)
            break
        elif input_choice == "3":
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            results = phone_book.search_by_timeframe(start_date, end_date)
            if not results:
                print("No contacts found.")
            for contact in results:
                print(f"{contact.first_name} {contact.last_name}, Phone: {contact.phone}")
                phone_book.log("Search", contact)
            break
        else:
            print("Invalid choice, please try again.")


def update_contact(phone_book):
    """
    Updates a contact's details based on phone number.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book containing the contact to update.
    """
    phone = input("Enter phone number of the contact to update: ")
    contact = phone_book.search_by_phone(phone)
    first_name = input("New First Name (or leave blank to keep current): ")
    last_name = input("New Last Name (or leave blank to keep current): ")
    email = input("New Email (or leave blank to keep current): ")
    address = input("New Address (or leave blank to keep current): ")
    phone_book.update(phone, first_name, last_name, email, address)
    phone_book.log("Update", contact)
    print(f"Contact with phone number {phone} updated.")


def delete_contact(phone_book):
    """
    Deletes a contact from the phone book by phone number.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book containing the contact to delete.
    """
    phone = input("Enter phone number of the contact to delete: ")
    contact = phone_book.search_by_phone(phone)
    phone_book.delete(phone)
    phone_book.log("Delete", contact)
    print(f"Deleted contact with phone number {phone}.")


def view_audit_history(phone_book):
    """
    Displays the audit history of operations performed on the phone book.

    Parameters:
    -----------
    phone_book : PhoneBook
        The phone book whose audit history is to be displayed.
    """
    history = phone_book.get_history()
    for log in history:
        print(log)


def main():
    """
    The main function that runs the phone book application, allowing users to perform operations
    like adding, viewing, searching, updating, and deleting contacts.
    """
    phone_book = PhoneBook()

    while True:
        try:
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

            print("\nEnter any key to continue...")
            input()

        except Exception as e:
            print(f"\nAn error occurred: {e}, please try again.")

# Run the main function
if __name__ == "__main__":
    main()
