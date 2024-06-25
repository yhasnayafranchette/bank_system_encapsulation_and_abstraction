# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from bank_account import BankAccount

class CNBankAccount(BankAccount):
    def __init__(self, account_number, account_name, account_type, balance=0.0, pin=1234, birthdate="", status="active"):
        self.__account_number = str(account_number)
        self.__account_name = str(account_name)
        self.__account_type = str(account_type)
        self.__balance = balance
        self.__pin = int(pin)
        self.__birthdate = str(birthdate)
        self.__status = str(status)
        
    @property
    def account_number(self):
        return self.__account_number    
    
    @property
    def account_name(self):
        return self.__account_name
    
    @property
    def pin(self):
        return self.__pin

    @property
    def balance(self):
        return self.__balance

    @property
    def birthdate(self):
        return self.__birthdate

    @property
    def account_type(self):
        return self.__account_type
    
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        self.__status = new_status

    @property
    def check_balance(self):
        return self.__balance
    
    def authenticate(self, entered_pin):
        return self.__pin == entered_pin

    def change_pin(self, new_pin):
        self.__pin = new_pin

    def deposit(self, amount, source='teller'):
        if self.__status == "active":
            if source == 'atm' and amount > 20000:
                print("ATM deposit limit exceeded. Please transact with a teller for higher amounts.")
            else:
                self.__balance += amount
                print(f"Deposit successful. Amount deposited: {amount}.")
        else:
            print("Account is locked. Transaction cannot proceed.")

    def withdraw(self, amount, source='teller'):
        if self.__status == "active":
            if source == 'atm' and amount > 20000:
                print("ATM withdrawal limit exceeded. Please transact with a teller for higher amounts.")
            elif self.__balance >= amount:
                self.__balance -= amount
                print(f"Withdrawal successful. Amount withdrawn: {amount}.")
            else:
                print("Insufficient balance.")
        else:
            print("Account is locked. Transaction cannot proceed.")