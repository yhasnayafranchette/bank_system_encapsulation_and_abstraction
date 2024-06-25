# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from bank_customer import BankCustomer
from bank_teller import BankTeller
from bank_manager import BankManager

class BankSystem():
    def __init__(self):
        self.logged_in_user = None

    def display_menu(self):
        if self.logged_in_user:
            if isinstance(self.logged_in_user, BankCustomer):
                print("\nUser Menu:")
                print("1. Request account")
                print("2. Perform transactions")
                print("3. Request Loan")
                print("4. Log out")
            elif isinstance(self.logged_in_user, BankManager):
                print("\nBank System Menu:")
                print("1. Approve account requests")
                print("2. Approve loan")
                print("3. Lock Account")
                print("4. Unlock Account")
                print("5. Approve account deactivation")
                print("6. Use ATM")
                print("7. Log out")
            elif isinstance(self.logged_in_user, BankTeller):
                print("\nBank System Menu:")
                print("1. Process account requests")
                print("2. Deactivate account")
                print("3. Teller Transaction for Customer")
                print("4. Transfer Loan")  
                print("5. Use ATM")
                print("6. Log out")
        else:
            print("\nWelcome to Bank Account System!")
            print("\nBank System Menu:")
            print("1. Register user")
            print("2. Log in")
            print("3. Exit")

    def register_user(self):
        first_name = input("Enter First name: ").title()
        middle_name = input("Enter Middle name: ").title()
        last_name = input("Enter Last name: ").title()
        fullname = f"{first_name} {middle_name} {last_name}"
        if BankCustomer.user_exists(fullname):
            print("User already registered.")
            return

        birthdate = self.get_valid_birthdate()
        role = "Customer"  
        monthly_salary = self.get_valid_salary()
        username = self.get_unique_username()
        password = self.get_valid_password()

        BankCustomer.update_users_list(fullname)
        BankCustomer.get_users()[fullname] = BankCustomer(fullname, username, password, birthdate, role, monthly_salary)
        print("--- CUSTOMER REGISTERED ---")

    def get_unique_username(self):
        while True:
            username = input("Enter username: ")
            if username not in BankCustomer.get_usernames():
                return username
            else:
                print("Username already taken. Please choose a different username.")

    def get_valid_password(self):
        while True:
            password = input("Enter password: ")
            if password not in BankCustomer.get_passwords():
                return password
            else:
                print("Passwords do not match. Please try again.")

    def validate_and_format_birthdate(self, birthdate):
        try:
            parts = birthdate.split()
            if len(parts) != 3:
                raise ValueError("Birthdate must be in 'Month Day, Year' format")
            
            month, day, year = parts
            months = ["January", "February", "March", "April", "May", "June", "July",
                      "August", "September", "October", "November", "December"]
            if month.capitalize() not in months or len(year) != 4:
                raise ValueError("Invalid birthdate format")
            
            day = day.strip(',')  
            formatted_birthdate = f"{month.capitalize()} {day}, {year}"
            return formatted_birthdate
        
        except ValueError as e:
            print(f"Invalid birthdate format: {e}. Please enter in 'Month Day, Year' format.")
            return None
        
    def get_valid_birthdate(self):
        while True:
            birthdate = input("Enter birthdate (Month Day, Year): ")
            formatted_birthdate = self.validate_and_format_birthdate(birthdate)
            if formatted_birthdate:
                return formatted_birthdate

    def get_valid_salary(self):
        while True:
            try:
                monthly_salary = float(input("Enter monthly salary: "))
                return monthly_salary
            except ValueError:
                print("Invalid input. Please enter a valid number for monthly salary.")

    def login(self):
        while True:
            user_type = input("Are you logging in as a Customer, Teller, or Manager? ").strip().lower()

            if user_type not in ['customer', 'teller', 'manager']:
                print("Invalid user type. Please enter 'Customer', 'Teller', or 'Manager'.")
                continue

            if user_type == 'customer':
                customers_usernames = BankCustomer.get_usernames()
                if not customers_usernames:
                    print("No customers registered. Please register first.")
                    return
            elif user_type == 'teller':
                tellers_usernames = BankTeller.get_tellers()
                if not tellers_usernames:
                    print("No tellers registered.")
                    return
            elif user_type == 'manager':
                managers_usernames = BankManager.get_managers()
                if not managers_usernames:
                    print("No managers registered. ")
                    return

            username = input("Enter username: ")
            password = input("Enter password: ")

            if user_type == 'customer':
                customers_usernames = BankCustomer.get_usernames()
                customers_passwords = BankCustomer.get_passwords()

                if username in customers_usernames and password in customers_passwords:
                    self.logged_in_user = customers_usernames[username]
                    print(f"Logged in as Customer: {self.logged_in_user.fullname}")
                else:
                    print("Invalid username or password for customer or user not registered.")

            elif user_type == 'teller':
                if username in BankTeller.get_tellers() and BankTeller.get_tellers()[username].authenticate(password):
                    self.logged_in_user = BankTeller.get_tellers()[username]
                    print(f"Logged in as Teller: {self.logged_in_user.fullname}")
                else:
                    print("Invalid username or password for teller.")

            elif user_type == 'manager':
                if username in BankManager.get_managers() and BankManager.get_managers()[username].authenticate(password):
                    self.logged_in_user = BankManager.get_managers()[username]
                    print(f"Logged in as Manager: {self.logged_in_user.fullname}")
                else:
                    print("Invalid username or password for manager.")
            break

    def logout(self):
        self.logged_in_user = None
        print("Logged out.")

    def process_account_requests(self):
        if isinstance(self.logged_in_user, BankTeller):
            teller_username = self.logged_in_user.username
            if teller_username in BankTeller.get_tellers():
                bank_teller = BankTeller.get_tellers()[teller_username]
                for customer_name, customer in BankCustomer.get_usernames().items():
                    if not customer.bank_account:
                        print(f"Processing account request for {customer.fullname}")
                        bank_teller.create_bank_account(customer)
            else:
                print("Teller not found.")
        else:
            print("Access denied. Please log in as a teller.")

    def approve_account_requests(self):
        if isinstance(self.logged_in_user, BankManager):
            manager_username = self.logged_in_user.username
            if manager_username in BankManager.get_managers():
                bank_manager = BankManager.get_managers()[manager_username]
                customers = list(BankCustomer.get_usernames().values())
                for i, customer in enumerate(customers):
                    print(f"{i}. {customer.fullname}")
                customer_index = int(input("Select customer by number: "))
                customer = customers[customer_index]
                print(f"Approving account request for {customer.fullname}")
                bank_manager.approve_account_creation(customer)
                print(f"Account creation approved for {customer.fullname}")
                customer.display_account_details()
            else:
                print("Manager not found.")
        else:
            print("Access denied. Please log in as a manager.")

    def perform_transactions(self):
        if isinstance(self.logged_in_user, BankCustomer):
            print("1. Transact with teller")
            print("2. Use ATM machine")
            choice = input("Enter choice: ")

            if choice == '1':
                self.logged_in_user.transact_with_teller()
            elif choice == '2':
                self.logged_in_user.use_atm()
            else:
                print("Invalid choice.")
        else:
            print("Access denied. Please log in as a customer.")

    def teller_transaction(self):
        if isinstance(self.logged_in_user, BankTeller):
            print("\nTeller Transaction Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            choice = input("Enter choice: ")

            if choice == '1':
                amount = float(input("Enter deposit amount: "))
                teller_username = input("Enter teller username: ")
                tellers= BankTeller.get_tellers()
                if teller_username in tellers:
                    teller = tellers[teller_username]
                    teller.bank_account.deposit(amount)
                else:
                    print("Teller not found.")
            elif choice == '2':
                amount = float(input("Enter withdrawal amount: "))
                teller_username = input("Enter teller username: ")
                tellers = BankTeller.get_tellers()
                if teller_username in tellers:
                    teller = tellers[teller_username]
                    teller.bank_account.withdraw(amount)
                else:
                    print("Teller not found.")
            elif choice == '3':
                teller_username = input("Enter teller username: ")
                tellers = BankTeller.get_tellers()
                if teller_username in tellers:
                    teller = tellers[teller_username]
                    balance = teller.bank_account.check_balance 
                    print(f"Current Balance: {balance}")
                else:
                    print("Teller not found.")
            else:
                print("Invalid choice.")
        else:
            print("Access denied. Please log in as a teller.")

    def manager_transaction(self):
        if isinstance(self.logged_in_user, BankManager):
            print("\nManager Transaction Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            choice = input("Enter choice: ")

            if choice == '1':
                amount = float(input("Enter deposit amount: "))
                manager_username = input("Enter manager username: ")
                managers = BankManager.get_managers()
                if manager_username in managers:
                    manager = managers[manager_username]
                    manager.bank_account.deposit(amount)
                else:
                    print("Manager not found.")
            elif choice == '2':
                amount = float(input("Enter withdrawal amount: "))
                manager_username  = input("Enter manager username: ")
                managers = BankManager.get_managers()
                if manager_username in managers:
                    manager = managers[manager_username]
                    manager.bank_account.withdraw(amount)
                else:
                    print("Manager not found.")
            elif choice == '3':
                manager_username = input("Enter manager username: ")
                managers = BankManager.get_managers()
                if manager_username in managers:
                    manager = managers[manager_username]
                    balance = manager.bank_account.check_balance 
                    print(f"Current Balance: {balance}")
                else:
                    print("Manager not found.")
            else:
                print("Invalid choice.")
        else:
            print("Access denied. Please log in as a manager.")