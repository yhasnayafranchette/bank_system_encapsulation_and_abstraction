# Laboratory Exercise #6 and #7: Encapsulation and Abstraction - DELA ROSA, SORIANO

from bank_system import BankSystem
from example_interaction_bank_account_bank_customer import manager_account
from example_interaction_bank_account_bank_customer import teller_account
from bank_customer import BankCustomer
from bank_teller import BankTeller
from bank_manager import BankManager

def main():
    bank_system = BankSystem()
    running = True

    while running:
        bank_system.display_menu()
        choice = input("Enter choice: ")

        if choice == '1':   
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankCustomer):
                    bank_system.logged_in_user.request_account()
                elif isinstance(bank_system.logged_in_user, BankManager):
                    bank_system.approve_account_requests()
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    bank_system.process_account_requests()
            else:
                bank_system.register_user()

        elif choice == '2':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankCustomer):
                    bank_system.perform_transactions()
                elif isinstance(bank_system.logged_in_user, BankManager):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        loan_amount = customer.requested_loan_amount
                        bank_manager = BankManager.get_managers()[bank_system.logged_in_user.username]
                        if bank_manager.approve_loan(customer, loan_amount):
                            print("Wait for the Bank Teller to transfer the loan.")
                        else:
                            print("Loan approval failed.")
                    else:
                        print("Customer not found.")
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        bank_system.logged_in_user.deactivate_account(customer)
                    else:
                        print("Customer not found.")
            else:
                bank_system.login()

        elif choice == '3':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankCustomer):
                    bank_system.logged_in_user.request_loan()
                elif isinstance(bank_system.logged_in_user, BankManager):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        bank_manager = BankManager.get_managers()[bank_system.logged_in_user.username]
                        bank_manager.lock_account(customer.bank_account)
                        print("Account locked")
                    else:
                        print("Customer not found.")
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        customer.transact_with_teller()
                    else:
                        print("Customer not found.")
            else:
                running = False

        elif choice == '4':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankCustomer):
                    bank_system.logout()
                elif isinstance(bank_system.logged_in_user, BankManager):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        bank_manager = BankManager.get_managers()[bank_system.logged_in_user.username]
                        bank_manager.unlock_account(customer.bank_account)
                        print("Account unlocked")
                    else:
                        print("Customer not found.")
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    customer_username = input("Enter customer username: ")
                    customers = BankCustomer.get_usernames()
                    if customer_username in customers:
                        customer = customers[customer_username]
                        teller = BankTeller.get_tellers()[bank_system.logged_in_user.username]
                        loan_amount = customer.requested_loan_amount
                        teller.transfer_loan(customer, loan_amount)
                    else:
                        print("Customer not found.")
            else:
                running = False

        elif choice == '5':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankManager):
                    teller_username = input("Enter teller username: ")
                    tellers = BankTeller.get_tellers()
                    if teller_username in tellers:
                        teller = tellers[teller_username]
                        bank_manager = BankManager.get_managers()[bank_system.logged_in_user.username]
                        bank_manager.approve_account_deactivation(teller, customer)
                    else:
                        print("Teller not found.")
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    bank_system.teller_transaction()
            else:
                running = False

        elif choice == '6':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankManager):
                    bank_system.manager_transaction()
                elif isinstance(bank_system.logged_in_user, BankTeller):
                    bank_system.logout()
            else:
                running = False

        elif choice == '7':
            if bank_system.logged_in_user:
                if isinstance(bank_system.logged_in_user, BankManager):
                    bank_system.logout()
            else:
                running = False
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()