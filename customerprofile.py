def customer_profile(con, customer_profile_id):
    """
    Displays customer profile options and handles various banking operations.
    """
    try:
        while True:
            print("Enter 1: Check Bank Balance \n2: Deposit Money \n3: Withdraw Money \n4: Transfer Money \n5: Account Statement \n6: Logout")

            choice = int(input())
            if choice == 1:
                with con.cursor() as cur:
                    cur.execute("SELECT current_balance FROM account WHERE account_id = %s", (customer_profile_id,))
                    print(f"Your account balance is: {cur.fetchone()[0]}")
            elif choice == 2:
                amount = float(input("Enter amount to deposit: "))
                with con.cursor() as cur:
                    cur.execute("SELECT current_balance FROM account WHERE account_id = %s", (customer_profile_id,))
                    new_balance = cur.fetchone()[0] + amount
                    cur.execute("UPDATE account SET current_balance = %s WHERE account_id = %s", (new_balance, customer_profile_id))
                    cur.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'deposit', %s)", (customer_profile_id, amount))
                    con.commit()
                    print(f"Rs. {amount} deposited successfully")
            elif choice == 3:
                amount = float(input("Enter amount to withdraw: "))
                with con.cursor() as cur:
                    cur.execute("SELECT current_balance FROM account WHERE account_id = %s", (customer_profile_id,))
                    current_balance = cur.fetchone()[0]
                    if amount > current_balance:
                        print("Insufficient funds")
                    else:
                        new_balance = current_balance - amount
                        cur.execute("UPDATE account SET current_balance = %s WHERE account_id = %s", (new_balance, customer_profile_id))
                        cur.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'withdraw', %s)", (customer_profile_id, amount))
                        con.commit()
                        print(f"Rs. {amount} withdrawn successfully")
            elif choice == 4:
                transfer_money(con, customer_profile_id)
            elif choice == 5:
                print_account_statement(con, customer_profile_id)
            elif choice == 6:
                break
            else:
                print("Please enter a correct option")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_account_statement(con, customer_profile_id):
    """
    Retrieves and prints the account statement for a customer.
    """
    try:
        with con.cursor() as cur:
            cur.execute("""
                SELECT transaction_type, amount, date_time
                FROM transactions
                WHERE account_id = %s
                ORDER BY date_time DESC
            """, (customer_profile_id,))
            
            transactions = cur.fetchall()
            for x in transactions:
                print(type(x[2]),x[2])

            cur.execute("""
                        SELECT current_balance FROM account 
                        where account_id = %s
                        """,(customer_profile_id,))
            
            current_balance = cur.fetchone()[0]
            print("Current balance is",current_balance)
            flag = True

            if transactions:
                print(f"\n{'Transaction Type':<20} {'Amount':<10} {'Date & Time':<20} {'Balance':>10}")
                print("="*65)
                for transaction in transactions:
                    print(f"{transaction[0]:<20} {transaction[1]:<10} {transaction[2]} {current_balance:>10}")
                    if transaction[0] == 'deposit':
                        current_balance -= transaction[1]
                    elif transaction[0] == "withdraw":
                        current_balance += transaction[1]
                    elif transaction[0] == "transfer_out"  :
                        current_balance += transaction[1]  
                    else:
                        current_balance -= transaction[1]  

                        
                print("="*65)
            else:
                print("No transactions found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def transfer_money(con, customer_profile_id):
    """
    Transfers money from the logged-in customer's account to another account.
    """
    try:
        recipient_account_number = int(input("Enter the recipient's account number: "))
        amount = float(input("Enter amount to transfer: "))
        
        with con.cursor() as cur:
            # Check if the recipient account exists
            cur.execute("SELECT account_id FROM account WHERE account_number = %s", (recipient_account_number,))
            recipient = cur.fetchone()
            
            if not recipient:
                print("The recipient's account number is not valid.")
                return
            
            recipient_account_id = recipient[0]
            
            # Check the sender's balance
            cur.execute("SELECT current_balance FROM account WHERE account_id = %s", (customer_profile_id,))
            sender_balance = cur.fetchone()[0]
            
            if amount > sender_balance:
                print("Insufficient funds")
                return
            
            # Update sender's balance
            new_sender_balance = sender_balance - amount
            cur.execute("UPDATE account SET current_balance = %s WHERE account_id = %s", (new_sender_balance, customer_profile_id))
            
            # Update recipient's balance
            cur.execute("SELECT current_balance FROM account WHERE account_id = %s", (recipient_account_id,))
            recipient_balance = cur.fetchone()[0]
            new_recipient_balance = recipient_balance + amount
            cur.execute("UPDATE account SET current_balance = %s WHERE account_id = %s", (new_recipient_balance, recipient_account_id))
            
            # Record the transfer in transactions table
            cur.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer_out', %s)", (customer_profile_id, amount))
            cur.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'transfer_in', %s)", (recipient_account_id, amount))
            
            con.commit()
            print(f"Rs. {amount} transferred successfully to account number {recipient_account_number}")
    except Exception as e:
        print(f"An error occurred: {e}")
