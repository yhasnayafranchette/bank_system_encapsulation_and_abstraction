# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from user import User
from cn_bank_account import CNBankAccount
from bank_teller import BankTeller
from bank_manager import BankManager

# Bank Manager Existing Accounts 
bank_manager = BankManager("Manager", "manager_username", "manager_password", "January 20, 1980", "Manager", 15000)
manager_monthly_salary = 15000
manager_account = CNBankAccount("A7G9T4H2", "Manager", "Payroll", manager_monthly_salary)
bank_manager.bank_account = manager_account

# Bank Teller Existing Accounts 
bank_teller = BankTeller("Teller", "teller_username", "teller_password", "March 21, 1990", "Teller", 10000.00, is_admin=True)
teller_monthly_salary = 10000.00  
teller_account = CNBankAccount("J5K2L8M3", "Teller", "Payroll", teller_monthly_salary)
bank_teller.bank_account = teller_account

# print(manager_account.balance)
# print(teller_account.balance)