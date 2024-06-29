from prettytable import PrettyTable

class Account:
    def __init__(self, acc_no, name, balance, address):
        self.acc_no = acc_no
        self.name = name
        self.balance = balance
        self.address = address
        
    def __str__(self):
        return f"{self.acc_no},{self.name},{self.balance},{self.address}"


class BankManagement:
    def __init__(self):
        self.accounts = []        

    def add_account(self, account):
        try:
            with open("info.txt", "r") as fp:
                for l in fp:
                    if str(account.acc_no) in l:
                        print("Account already exists.")
                        break
                else:
                    self.accounts.append(account)
                    with open("info.txt", "a") as fp_append:
                        fp_append.write(str(account) + "\n")
                    print("Account added successfully!")
        except Exception as fe:
            print("An error occurred:", fe)


    def delete_account(self, acc_no):
        try:
            found = False
            with open("info.txt", "r") as fp:
                lines = fp.readlines()
            with open("info.txt", "w") as fp:
                for l in lines:
                    if l.split(",")[0] != acc_no:
                        fp.write(l)
                    else:
                        found = True
            return found
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print("An error occurred:", e)
            return False

    def check_balance(self, acc_no):
        try:
            account = self.search_account(acc_no)
            if account:
                return account.balance
            else:
                return None
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def search_account(self, acc_no):
        try:
            with open("info.txt", "r") as fp:
                for line in fp:
                    data = line.strip().split(",")
                    if data[0] == acc_no:
                        return Account(data[0], data[1], float(data[2]), data[3])
            return None
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None

    def show_all_accounts(self):
        try:
            with open("info.txt", "r") as fp:
                table = PrettyTable(["Account No", "Name", "Balance", "Address"])
                for line in fp:
                    data = line.strip().split(",")
                    table.add_row([data[0], data[1], data[2], data[3]])
                print(table)
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print("An error occurred:", e)


    def update_account(self, acc_no, field, new_value):
        try:
            account = self.search_account(acc_no)
            if account:
                if field == 'name':
                    account.name = new_value
                elif field == 'balance':
                    account.balance = float(new_value)
                elif field == 'address':
                    account.address = new_value
                else:
                    print("Invalid field!")
                    return False

                with open("info.txt", "r") as fp:
                    lines = fp.readlines()
                with open("info.txt", "w") as fp:
                    for line in lines:
                        if line.split(",")[0] == acc_no:
                            line = f"{account.acc_no},{account.name},{account.balance},{account.address}\n" #{account.pin}
                        fp.write(line)
                return True
            else:
                print("Account not found!")
                return False
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print("An error occurred:", e)
            return False
       

    def credit(self, acc_no, amount):
        try:
            account = self.search_account(acc_no)
            if account:
                account.balance += amount
                with open("info.txt", "r") as fp:
                    lines = fp.readlines()
                with open("info.txt", "w") as fp:
                    for l in lines:
                        if l.split(",")[0] == acc_no:
                            l = f"{account.acc_no},{account.name},{account.balance},{account.address}\n"
                        fp.write(l)
                return True
            return False
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print("An error occurred:", e)
            return False

    def debit(self, acc_no, amount):
        try:
            account = self.search_account(acc_no)
            if account and account.balance >= amount:
                account.balance -= amount
                with open("info.txt", "r") as fp:
                    lines = fp.readlines()
                with open("info.txt", "w") as fp:
                    for line in lines:
                        if line.split(",")[0] == acc_no:
                            line = f"{account.acc_no},{account.name},{account.balance},{account.address}\n"
                        fp.write(line)
                return True
            return False
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print("An error occurred:", e)
            return False
        
    def pin_change(self, acc_no, new_pin):
        try:
            account = self.search_account(acc_no)
            if account:
                account.pin = new_pin
                return True
            return False    
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print("An error occurred:", e)
            return None
        
    def money_transfer(self, sender_acc_no, receiver_acc_no, amount):
        try:
            sender_exists = False
            receiver_exists = False
            with open("info.txt", "r") as fp:
                for l in fp:
                    if sender_acc_no in l:
                        sender_exists = True
                    if receiver_acc_no in l:
                        receiver_exists = True

            if not sender_exists:
                print(f"Sender account {sender_acc_no} not found.")
                return False
            if not receiver_exists:
                print(f"Receiver account {receiver_acc_no} not found.")
                return False

            self.debit(sender_acc_no, amount)
            if self.credit(receiver_acc_no, amount):
                return True
            else:
                self.credit(sender_acc_no, amount)
                return False
        except FileNotFoundError:
            print("Transaction failed (try again).")
            return False    


def main():
    bank = BankManagement()
    while True:
        print("\nWelcome to Bank Management System")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username == "Praphull" and password == "7777":
                while True:
                    print("    \nAdmin Menu    ")
                    print("            1. Add Account")
                    print("            2. Delete Account")
                    print("            3. Check Balance")
                    print("            4. Search Account")
                    print("            5. Show All Accounts")
                    print("            6. Update")
                    print("            7. Transaction Details")
                    print("            7. Go Back")
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == '1':
                        try:
                            acc_no = input("Enter Account No: ")
                            name = input("Enter Name: ")
                            balance = float(input("Enter Initial Balance: "))
                            if balance>0:
                                address = input("Enter Address: ")
                                account = Account(acc_no, name, balance, address)
                                bank.add_account(account)
                            else:
                                print("Your Balance is Negative")    
                        except ValueError:
                            print("Invalid input. Please enter a valid number for balance.")
                        
                    elif admin_choice == '2':
                        acc_no = input("Enter Account No to delete: ")
                        if bank.delete_account(acc_no):
                            print("Account deleted successfully!")
                        else:
                            print("Account not found!")
                    elif admin_choice == '3':
                        acc_no = input("Enter Account No: ")
                        balance = bank.check_balance(acc_no)
                        if balance is not None:
                            print(f"Balance: {balance}")
                        else:
                            print("Account not found!")
                    elif admin_choice == '4':
                        acc_no = input("Enter Account No: ")
                        account = bank.search_account(acc_no)
                        if account:
                            print(f"Account No: {account.acc_no} | Name: {account.name} | Balance: {account.balance}")
                        else:
                            print("Account not found!")
                    elif admin_choice == '5':
                        bank.show_all_accounts()

                    elif admin_choice == '6':
                        acc_no = input("Enter Account No to update: ")
                        field = input("Enter field to update (name/balance/address/pin): ")
                        new_value = input("Enter new value: ")
                        if bank.update_account(acc_no, field, new_value):
                            print("Account updated successfully!")
                        else:
                            print("Failed to update account!")

                    elif admin_choice == '7':
                        break
                    else:
                        print("Invalid choice!")
            else:
                print("\nInvalid username or password!")
        elif choice == '2':
            while True:
                print("")
                print("         ! Welcome to User Menu !")
                print("         1. Create New Account")
                print("         2. Check Balance")
                print("         3. Credit")
                print("         4. Debit")
                print("         5. Pin Change")
                print("         6. Money Transfer")
                print("         7. Go Back..")

                user_choice=input("Enter User Choice :")
                if user_choice=='1':
                    try:
                            acc_no = input("Enter Account No: ")
                            name = input("Enter Name: ")
                            balance = float(input("Enter Initial Balance: "))
                            if balance>0:
                                address = input("Enter Address: ")
                                account = Account(acc_no, name, balance, address)
                                bank.add_account(account)
                            else:
                                print("Your Balance is Negative")    
                    except ValueError:
                            print("Invalid input. Please enter a valid number for balance.")

                elif user_choice=='2':
                    acc_no = input("Enter Account No: ")
                    account = bank.search_account(acc_no)
                    if account:
                        print(f"Balance: {account.balance}")
                    else:
                        print("Account not found!")

                elif user_choice=='3':
                    try:
                        acc_no = input("Enter Account No: ")
                        amount = float(input("Enter amount to credit: "))
                        if bank.credit(acc_no, amount):
                            print("Amount credited successfully!")
                        else:
                            print("Account not found or credit failed!")
                    except ValueError:
                        print("Invalid Input...")

                elif user_choice=='4':
                    try:
                        acc_no=input("Enter Account No: ")
                        amount=float(input("Enter Amount to Debit: "))
                        if bank.debit(acc_no,amount):
                            print("Amount Debit Successfully !") 
                        else:
                            print("Account not found or Debit Failed!") 
                    except ValueError:
                        print("Invalid Input.") 

                elif user_choice=='5':
                    try:
                        acc_no=input("Enter Your Account: ")
                        new_pin=input("Enter New PIN: ")
                        if bank.pin_change(acc_no,new_pin):
                            print("Pin Change Successfully...")
                        else:
                            print("Account not Found , PIN change Failed.") 
                    except ValueError:
                        print("Invalid Input!")           

                elif user_choice=='6':
                    try:
                        sender_acc_no=input("Enter Sender Account No: ")
                        receiver_acc_no=input("Enter Reciver Account No: ")
                        amount=float(input("Enter Amount to Transfer: "))
                        if bank.money_transfer(sender_acc_no,receiver_acc_no,amount):
                            print("Money Transfer Successfully !")
                        else:
                            print("Money Transfer Failed")
                    except ValueError:
                        print("Invalid Input...")            

                elif user_choice=='7':
                    break
        elif choice==3:
            break
        else:
            print("Invalid Choice...")        

if __name__ == "__main__":
        main()        