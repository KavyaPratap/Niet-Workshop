class Account:
    def __init__(self, account_number, account_holder_id, balance=0.0):
        self._account_number = account_number
        self._balance = balance
        self._account_holder_id = account_holder_id

    @property
    def account_number(self):
        return self._account_number
    @property
    def balance(self):
        return self._balance
    @property
    def account_holder_id(self):
        return self._account_holder_id
    def display_details(self):
        return f"Acc No: {self._account_number}, Bal: Rs{self._balance:.2f}"

class SavingsAccount(Account):
    def __init__(self, account_number, account_holder_id, balance=0.0, interest_rate=0.01):
        super().__init__(account_number, account_holder_id, balance)
        self._interest_rate = interest_rate
    @property
    def interest_rate(self):
        return self._interest_rate
    @interest_rate.setter
    def interest_rate(self, value):
        self._interest_rate = value if value >= 0 else self._interest_rate
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    def withdraw(self, amount):
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            return True
        return False
    def apply_interest(self):
        self._balance += self._balance * self._interest_rate
    def display_details(self):
        return f"{super().display_details()}, Int Rate: {self._interest_rate:.2%}"

class CheckingAccount(Account):
    def __init__(self, account_number, account_holder_id, balance=0.0, overdraft_limit=0.0):
        super().__init__(account_number, account_holder_id, balance)
        self._overdraft_limit = overdraft_limit
    @property
    def overdraft_limit(self):
        return self._overdraft_limit
    
    @overdraft_limit.setter
    def overdraft_limit(self, value):
        self._overdraft_limit = value if value >= 0 else self._overdraft_limit
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= -self._overdraft_limit:
            self._balance -= amount
            return True
        return False
    def display_details(self) -> str:
        return f"{super().display_details()}, OD Limit: Rs{self._overdraft_limit:.2f}"

class Customer:
    def __init__(self, customer_id, name, address):
        self._customer_id = customer_id
        self._name = name
        self._address = address
        self._account_numbers = []
    @property
    def customer_id(self):
        return self._customer_id
    @property
    def name(self):
        return self._name
    @property
    def address(self):
        return self._address
    @property
    def account_numbers(self):
        return list(self._account_numbers)
    def add_account_number(self, account_number):
        if account_number not in self._account_numbers:
            self._account_numbers.append(account_number)
    def display_details(self):
        return f"Cust ID: {self._customer_id}, Name: {self._name}, Accs: {len(self._account_numbers)}"

class Bank:
    _next_account_number = 1000
    def __init__(self):
        self._customers = {}
        self._accounts = {}
    def add_customer(self, customer):
        if customer.customer_id not in self._customers:
            self._customers[customer.customer_id] = customer
            return True
        return False
    def remove_customer(self, customer_id):
        if customer_id in self._customers and not self._customers[customer_id].account_numbers:
            del self._customers[customer_id]
            return True
        return False
    def create_account(self, customer_id, account_type, initial_balance=0.0, **kwargs):
        if customer_id not in self._customers:
            return None
        customer = self._customers[customer_id]
        account_number = str(Bank._next_account_number)
        Bank._next_account_number += 1
        account = None
        if account_type == "savings":
            account = SavingsAccount(account_number, customer_id, initial_balance, kwargs.get("interest_rate", 0.01))
        elif account_type == "checking":
            account = CheckingAccount(account_number, customer_id, initial_balance, kwargs.get("overdraft_limit", 0.0))
        
        if account:
            self._accounts[account_number] = account
            customer.add_account_number(account_number)
        return account
    def deposit(self, account_number, amount):
        if account_number in self._accounts:
            return self._accounts[account_number].deposit(amount)
        return False
    def withdraw(self, account_number, amount):
        if account_number in self._accounts:
            return self._accounts[account_number].withdraw(amount)
        return False
    def transfer_funds(self, from_acc_num, to_acc_num, amount):
        if from_acc_num in self._accounts and to_acc_num in self._accounts:
            from_account = self._accounts[from_acc_num]
            to_account = self._accounts[to_acc_num]
            if from_account.withdraw(amount):
                to_account.deposit(amount)
                return True
        return False
    def get_customer_accounts(self, customer_id):
        if customer_id in self._customers:
            return [self._accounts[acc_num] for acc_num in self._customers[customer_id].account_numbers if acc_num in self._accounts]
        return []
    def display_all_customers(self):
        for c in self._customers.values():
            print(c.display_details())
    def apply_all_interest(self):
        for a in self._accounts.values():
            if isinstance(a, SavingsAccount):
                a.apply_interest()

bank = Bank()

while True:
    print("\nBanking System Menu:")
    print("1. Add Customer")
    print("2. Create Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer Funds")
    print("6. View Customer Accounts")
    print("7. Apply Interest")
    print("8. Display All Customers")
    print("9. Exit") 

    choice = input("Enter your choice: ")

    if choice == '1':
        cid = input("Enter customer ID: ")
        name = input("Enter customer name: ")
        addr = input("Enter customer address: ")
        if bank.add_customer(Customer(cid, name, addr)):
            print("Customer added.")
        else:
            print("Customer ID already exists.")
    
    elif choice == '2':
        cid = input("Enter customer ID: ")
        atype = input("Enter account type (savings/checking): ").lower()
        bal = float(input("Enter initial balance: "))
        
        kwargs = {}
        if atype == "savings":
            kwargs["interest_rate"] = float(input("Enter interest rate (e.g., 5 for 5%): ")) / 100
        elif atype == "checking":
            kwargs["overdraft_limit"] = float(input("Enter overdraft limit (0.0): "))

        acc = bank.create_account(cid, atype, bal, **kwargs)
        if acc:
            print(f"Account created: {acc.display_details()}")
        else:
            print("Failed to create account (customer not found or invalid account type).")

    elif choice == '3' or choice == '4':
        cid = input("Enter customer ID: ")
        customer_accounts = bank.get_customer_accounts(cid)
        if not customer_accounts:
            print("No accounts found for this customer or customer ID invalid.")
            continue

        print(f"\nAccounts for Customer ID {cid}:")
        for i, acc in enumerate(customer_accounts):
            print(f"{i+1}. {acc.display_details()}")
        
        acc_choice = input("Select account number (from list above): ")
        try:
            acc_idx = int(acc_choice) - 1
            if 0 <= acc_idx < len(customer_accounts):
                selected_account = customer_accounts[acc_idx]
                amount = float(input("Enter amount: "))
                if choice == '3':
                    if bank.deposit(selected_account.account_number, amount):
                        print("Deposit successful.")
                    else:
                        print("Deposit failed (invalid amount).")
                else:
                    if bank.withdraw(selected_account.account_number, amount):
                        print("Withdrawal successful.")
                    else:
                        print("Withdrawal failed (insufficient funds or invalid amount).")
            else:
                print("Invalid account selection.")
        except ValueError:
            print("Invalid input.")

    elif choice == '5':
        from_acc_num = input("Enter source account number: ")
        to_acc_num = input("Enter destination account number: ")
        amt = float(input("Enter amount to transfer: "))
        if bank.transfer_funds(from_acc_num, to_acc_num, amt):
            print("Transfer successful.")
        else:
            print("Transfer failed.")

    elif choice == '6':
        cid = input("Enter customer ID: ")
        accs = bank.get_customer_accounts(cid)
        if accs:
            print(f"Accounts for Customer ID {cid}:")
            for a in accs:
                print(a.display_details())
        else:
            print("No accounts found for this customer or customer ID invalid.")

    elif choice == '7':
        bank.apply_all_interest()
        print("Interest applied to all savings accounts.")

    elif choice == '8': 
        print("\nAll Customers:")
        bank.display_all_customers()

    elif choice == '9': 
        print("Exiting Banking System...")
        break

    else:
        print("Invalid choice. Please try again.")
