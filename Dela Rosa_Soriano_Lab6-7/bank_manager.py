# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from bank_teller import BankTeller
from bank_account import BankAccount
from bank_customer import BankCustomer

class BankManager(BankTeller):
    __managers = {}  

    @classmethod
    def get_managers(cls):
        return cls.__managers

    def __init__(self, fullname, username, password, birthdate, role, monthly_salary, is_admin=True):
        super().__init__(fullname, username, password, birthdate, role, monthly_salary, is_admin=True, bank_account=None)
        self.__username = username
        self.__password = password 
        self.__is_admin = is_admin  
        BankManager.get_managers()[username] = self  

    @property
    def is_admin(self):
        return self.__is_admin
    
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    def authenticate(self, password):  
        return self.__password == password
    
    def approve_account_deactivation(self, teller, customer):
        if teller.is_admin:
            if customer.bank_account.status == "pending_deactivation":
                customer.bank_account.status = "inactive"
                print("Account deactivation approved.")
            else:
                print("No pending account deactivation requests found.")
        else:
            print("Approval failed. Teller is not an admin.")

    def approve_account_creation(self, customer):
        if isinstance(customer.bank_account, BankAccount):
            customer.bank_account.status = "active"
            print("Account creation approved. Account is now active.")
        else:
            print("No bank account associated with the customer.")
    
    def approve_loan(self, customer, amount):
        if customer is not None and isinstance(customer, BankCustomer):
            if amount <= customer.monthly_salary * 4 and not customer.has_existing_loan:
                print("Loan approved successfully.")
                customer.has_existing_loan = True 
                return True
            else:
                if amount > customer.monthly_salary * 4:
                    print("Requested amount exceeds 400% of monthly salary.")
                elif customer.has_existing_loan:
                    print("Customer already has an existing loan.")
                return False
        else:
            print("Access denied. Please provide a valid customer object.")
            return False

    def lock_account(self, account):
        if isinstance(account, BankAccount):
            account.locked = "locked"
            print(f"Account {account.account_number} locked successfully.")
        else:
            print("Invalid account provided.")

    def unlock_account(self, account):
        if isinstance(account, BankAccount):
            account.locked = "active"
            print(f"Account {account.account_number} unlocked successfully.")
        else:
            print("Invalid account provided.")