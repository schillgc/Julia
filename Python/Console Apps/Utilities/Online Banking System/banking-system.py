import os
import postal_address
import re


class Account:
    type: str = None
    balance: float = 0.00


class Customer:
    name: str = input("Customer's NAME: ")
    address = postal_address.address.Address
    social_security_number = re.compile(str(r'^\d{3}-\d{2}-\d{4}$'), input("Customer's SOCIAL SECURITY NUMBER: "))
    credit_rating: int = input("Customer's CREDIT RATING: ")


class Transaction:
    originator: str = None
    amount: float = 0.00


# Collections
transactions = Transaction.originator, Transaction.amount

demographics = [
    Customer.name,
    Customer.address,
]

protected_information = [
    Customer.social_security_number,
    Customer.credit_rating,
]

Account = [
    transactions,
    demographics,
    protected_information,
    Account.balance,
    Account.type,
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def request_balance():
    print("Balance: $" + str(Account.balance))


def deposit():
    clear_screen()

    Transaction.amount = input("How much do you wish to deposit?  $")
    Account[3] += float(Transaction.amount)

    request_balance()


def withdrawal():
    clear_screen()

    Transaction.amount = input("How much do you wish to withdrawal?  $")
    Account[3] -= float(Transaction.amount)

    request_balance()


def new_account():
    Account[4] = input("""
        'PERSONAL'
        '-----------------'
        'Personal Checking'
        'Personal Savings'
        'Personal Credit'
        'Personal Loan'
        '-----------------'

        'BUSINESS'
        '-----------------'
        'Business Checking'
        'Business Savings'
        'Business Credit'
        'Business Loan'
        '-----------------'

        'INVESTMENT'
        '-----------------'
        'IRA'
        'Custodial'
        'Real Estate'
        '-----------------'


Account TYPE """)


def tellers_menu():
    clear_screen()

    print("How may we proceed?")
    print("""
Enter 'NEW' to open a new account.
Enter 'DEPOSIT' to deposit into an account.
Enter 'WITHDRAWAL' to withdrawal from an account.
Enter 'BALANCE' to view account balance.
Enter 'EXIT' to sign-out.
""")

    while True:
        tellers_input = input("> ")

        if tellers_input.upper() == 'EXIT':
            break

        elif tellers_input.upper() == 'NEW':
            new_account()
            continue

        elif tellers_input.upper() == 'DEPOSIT':
            deposit()
            continue

        elif tellers_input.upper() == 'WITHDRAWAL':
            withdrawal()
            continue

        elif tellers_input.upper() == 'BALANCE':
            request_balance()
            continue


tellers_menu()
