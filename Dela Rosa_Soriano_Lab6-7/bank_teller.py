# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

import uuid 
from user import User
from cn_bank_account import CNBankAccount 
from bank_customer import BankCustomer      

class BankTeller(User):
    __tellers = {}  
    __teller_count = 0
    
    @classmethod
    def get_tellers(cls):
        return cls.__tellers

    def __init__(self, fullname, username, password, birthdate, role, monthly_salary, is_admin=False, bank_account=None):
        self.__fullname = str(fullname)
        self.__birthdate = birthdate
        self.__role = str(role)
        self.__monthly_salary = float(monthly_salary)
        self.__username = username
        self.__password = password  
        self.__is_admin = is_admin 
        BankTeller.__teller_count += 1
        self.__teller_id = BankTeller.__teller_count
        BankTeller.get_tellers()[username] = self  

    @property
    def fullname(self):
        return self.__fullname
    
    @property
    def birthdate(self):
        return self.__birthdate
    
    @property
    def monthly_salary(self):
        return self.__monthly_salary
    
    @property
    def is_admin(self):
        return self.__is_admin
    
    @property
    def username(self):
        return self.__username

    @property
    def teller_id(self):
        return self.__teller_id
    
    @property
    def password(self):
        return self.__password
    
    @property
    def role(self):
        return self.__role

    def authenticate(self, password): 
        return self.__password == password
        
    def create_bank_account(self, customer):
        account_number = (str(uuid.uuid4())[:8]).upper()
        account_name = f"{customer.fullname}'s Savings Account"
        account_type = "savings"

        if not customer.bank_account:
            if isinstance(customer, BankCustomer):
                customer.bank_account = CNBankAccount(account_number, account_name, account_type, birthdate=customer.birthdate, status="pending")
                print(f"Please wait for Manager's Approval.")
            else:
                print("Invalid account type for this user.")
        else:
            print("User already has an account.")

    def deactivate_account(self, customer):
        if isinstance(customer, BankCustomer):
            if self.__is_admin:
                customer.bank_account.status = "pending_deactivation"
                print("Account deactivation requested. Waiting for manager's approval.")
            else:
                print("Access denied. Only admin tellers can request account deactivation.")
    
    def deposit(self, amount, source='teller'):
        if self.__status == "active":
            if self.__account_type == "Payroll" and source != 'atm':
                print("Payroll accounts can only use the ATM for transactions.")
            elif source == 'atm' and amount > 20000:
                print("ATM deposit limit exceeded. Please transact with a teller for higher amounts.")
            else:
                self.__balance += amount
                print(f"Deposit successful. New balance: {self.__balance}")
        else:
            print("Account is locked. Transaction cannot proceed.")
    
    def withdraw(self, amount, source='teller'):
        if self.__status == "active":
            if self.__account_type == "Payroll" and source != 'atm':
                print("Payroll accounts can only use the ATM for transactions.")
            elif source == 'atm' and amount > 20000:
                print("ATM withdrawal limit exceeded. Please transact with a teller for higher amounts.")
            elif self.__balance >= amount:
                self.__balance -= amount
                print(f"Withdrawal successful. New balance: {self.__balance}")
            else:
                print("Insufficient balance.")
        else:
            print("Account is locked. Transaction cannot proceed.")
    
    def customer_check_balance(self, customer, account_number):
        if customer.bank_account:
            if self.__verify_account(customer, account_number, customer.birthdate):
                return customer.bank_account.check_balance()
            else:
                print("Account verification failed.")
                return None
        else:
            print("Customer does not have an account.")
            return None
    
    def verify_account(self, customer, account_number, birthdate):
        if customer.bank_account and customer.bank_account.account_number == account_number and customer.bank_account.birthdate == birthdate:
            print("Account verification successful.")
            return True
        else:
            print("Account verification failed.")
            return False
    
    def transfer_loan(self, customer, amount):
        if customer.bank_account:
            if customer.bank_account.account_type == "savings": 
                print("Bank Teller is transferring the {} loan to {}'s account.".format(amount, customer.fullname))
                print("Loan amount transferred to {}'s account.".format(customer.fullname))
                customer.bank_account.deposit(amount)
            else:
                print("Customer does not have a savings account.")
        else:
            print("Customer does not have a bank account.")