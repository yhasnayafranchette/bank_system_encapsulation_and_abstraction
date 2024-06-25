# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from user import User
from cn_bank_account import CNBankAccount

class BankCustomer(User):
    __users= {} 
    __usernames = {}
    __passwords ={}

    @classmethod
    def get_users(cls):
        return cls.__users
    
    @classmethod
    def update_users_list(cls, name):
        cls.__users[name] = name  

    @classmethod
    def user_exists(cls, name):
        return name in cls.__users

    @classmethod
    def get_usernames(cls):
        return cls.__usernames  
    
    @classmethod
    def get_passwords(cls):
        return cls.__passwords

    def __init__(self, fullname, username, password, birthdate, role, monthly_salary):
        self.__fullname = str(fullname)
        self.__birthdate = birthdate
        self.__role = str(role)
        self.__monthly_salary = float(monthly_salary)
        self.__bank_account = None
        self.__has_existing_loan = False
        self.__username = username
        self.__password = password
        BankCustomer.get_usernames()[username] = self 
        BankCustomer.get_passwords()[password] = self 
        self.requested_loan_amount = None 
        self.__status = None  
    
    @property
    def fullname(self):
        return self.__fullname
    
    @fullname.setter
    def fullname(self):
        pass
    
    @property
    def birthdate(self):
        return self.__birthdate
    
    @birthdate.setter
    def birthdate(self):
        pass
    
    @property
    def monthly_salary(self):
        return self.__monthly_salary
    
    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def bank_account(self):
        return self.__bank_account
    
    @bank_account.setter
    def bank_account(self, account):
        self.__bank_account = account

    @property
    def has_existing_loan(self):
        return self.__has_existing_loan

    @has_existing_loan.setter
    def has_existing_loan(self, value):
        self.__has_existing_loan = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self):
        pass

    def transact_with_teller(self):
        if isinstance(self.bank_account, CNBankAccount) and self.bank_account.status == "active":
            account_number = input("Enter your account number: ")
            if account_number == self.bank_account.account_number:
                birthdate = input("Enter your birthdate (Month Day, Year): ").capitalize()
                if birthdate == self.bank_account.birthdate:
                    while True:
                        print("Teller Menu: 1) Deposit 2) Withdraw 3) Check Balance 4) Exit")
                        teller_choice = input("Enter choice: ")
                        if teller_choice == '1':
                            amount = float(input("Enter amount to deposit: "))
                            self.bank_account.deposit(amount, source='teller')  
                        elif teller_choice == '2':
                            amount = float(input("Enter amount to withdraw: "))
                            self.withdraw_with_verification(amount)  
                        elif teller_choice == '3':
                            self.check_balance_with_verification()  
                        elif teller_choice == '4':
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Birthdate does not match.")
            else:
                print("Account number does not match.")
        else:
            print("Customer account is not active or does not exist.")

    def withdraw_with_verification(self, amount):
        withdrawal_birthdate = input("Enter your birthdate (Month Day, Year) for withdrawal verification: ").capitalize()
        
        if withdrawal_birthdate == self.bank_account.birthdate:
            self.bank_account.withdraw(amount, source='teller')
        else:
            print("Birthdate for withdrawal verification does not match.")

    def check_balance_with_verification(self):
        balance_birthdate = input("Enter your birthdate (Month Day, Year) for balance check verification: ").capitalize()
        if balance_birthdate == self.bank_account.birthdate:
            print(f"Balance: {self.bank_account.check_balance}")
        else:
            print("Birthdate for balance check verification does not match.")

    def use_atm(self):
        if self.__bank_account:
            entered_pin = int(input("Enter PIN to access ATM: "))
            
            if self.__bank_account.authenticate(entered_pin):
                print("PIN authenticated successfully.")
                print("ATM transaction initiated.")
                while True:
                    print("ATM Menu: 1) Deposit 2) Withdraw 3) Check Balance 4) Change PIN 5) Exit")
                    atm_choice = input("Enter choice: ")
                    if atm_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        self.__bank_account.deposit(amount, source='atm')
                    elif atm_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        self.__bank_account.withdraw(amount, source='atm')
                    elif atm_choice == '3':
                        print(f"Balance: {self.__bank_account.check_balance}")
                    elif atm_choice == '4':
                        new_pin = int(input("Enter new PIN: "))
                        self.__bank_account.change_pin(new_pin)
                        print("PIN changed successfully.")
                    elif atm_choice == '5':
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Invalid PIN. Access denied.")
        else:
            print("Customer does not have an account.")

    def display_account_details(self):
        if self.bank_account:
            if self.bank_account.status == "active":
                print("\nACCOUNT DETAILS:")
                print(f"Account Number: {self.bank_account.account_number}")
                print(f"Account Name: {self.bank_account._CNBankAccount__account_name}")
                print(f"Account Type: {self.bank_account._CNBankAccount__account_type}")
                print(f"Account Balance: {self.bank_account._CNBankAccount__balance}")
                print(f"Account PIN: {self.bank_account._CNBankAccount__pin}")
                print(f"Account Birthdate: {self.bank_account.birthdate}")
                print(f"Account Status: {self.bank_account.status}")
            else:
                print("Account is not active.")
        else:
            print("No bank account associated with the customer.")

    def request_account(self):
        if not self.bank_account:
            print("Account request made.")
            print("Please wait for the Bank Teller to process your account.")
        else:
            print("Customer already has an account.")
            self.display_account_details()

    def request_loan(self):
        if not self.bank_account:
            print("Loan request cannot be made without an account.")
        elif self.__has_existing_loan:
            print("Loan request denied. Existing loan detected.")
        else:
            self.requested_loan_amount = float(input("Enter loan amount: "))
            print("Loan request made.")
            print("Wait for Manager's approval.")
            return self.requested_loan_amount